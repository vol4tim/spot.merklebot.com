<template>
  <div>
    <div>
      <input
        type="file"
        @change="onFileChanged($event)"
      >
    </div>
    <div>status: {{ status }}</div>
    <div :class="{width: FRAME_WIDTH}">
      <div ref="stage" class="stage" />
      <div v-if="frameMax>0" class="mt-10 mb-10">
        <vue-slider v-model="frameNum" :max="frameMax" :drag-on-click="true" @change="sliderChooseFrame" />
        <div class="mt-4">
          <button class="rounded bg-blue-500 focus:outline-none m-2 p-2" @click="()=>{isPlaying=!isPlaying}">
            <i class="fa fa-play fa-2x text-white">
              {{ isPlaying?"Stop":"Play" }}
            </i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as THREE from 'three'
import { LoaderUtils } from 'three'
import { XacroLoader } from 'xacro-parser'
import { open } from 'rosbag'
import URDFLoader from 'urdf-loader'
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'

import { defineComponent, ref, onMounted } from '@nuxtjs/composition-api'

const FRAME_WIDTH = 800
const FRAME_HEIGHT = 500

export default defineComponent({
  components: { VueSlider },
  props: ['rosUrl', 'urdfUrl'],
  setup (props) {
    console.log(props)
    // const robotSocketLink = props.rosUrl
    const file = ref(null)
    const url = props.urdfUrl
    const status = ref('wait')
    const stage = ref(null)
    const frameNum = ref(0)
    const frameMax = ref(0)
    const isPlaying = ref(false)
    const timerId = ref(null)

    const topicsData = []

    const initialRobotPositionOffset = ref(null)
    const bodyTf = ref(null)
    const robotJoints = ref(null)
    const xacroLoader = new XacroLoader()

    const scene = new THREE.Scene()
    const geometry = new THREE.PlaneGeometry(8, 8)
    const material = new THREE.MeshBasicMaterial({ color: '#BBBBBB', side: THREE.DoubleSide })
    const plane = new THREE.Mesh(geometry, material)

    const camera = new THREE.PerspectiveCamera(
      80,
      4 / 3,
      0.1,
      1000
    )
    const renderer = new THREE.WebGLRenderer({ antialias: true })
    const light = new THREE.DirectionalLight('hsl(0, 100%, 100%)')
    const axes = new THREE.AxesHelper(5)
    let robot = null

    camera.position.z = -2.3
    camera.position.y = 1.6
    camera.position.x = -3.8
    camera.rotation.y = -Math.PI / 2 - 0.4

    plane.rotation.x = Math.PI / 2
    plane.position.y = 0

    scene.add(camera)
    scene.add(light)
    // scene.add(cube)
    scene.add(axes)
    scene.add(plane)

    xacroLoader.load(url, (xml) => {
      const urdfLoader = new URDFLoader()
      urdfLoader.workingPath = LoaderUtils.extractUrlBase(url)

      robot = urdfLoader.parse(xml)

      robot.rotation.x = -Math.PI / 2
      scene.add(robot)
      status.value = 'urdf loaded'
    })

    renderer.setSize(FRAME_WIDTH, FRAME_HEIGHT)
    light.position.set(5, 5, 0)

    scene.background = new THREE.Color('hsl(0, 100%, 100%)')

    const animate = () => {
      // requestAnimationFrame(animate)
      // renderer.render(scene, camera)
      setTimeout(function () {
        requestAnimationFrame(animate)
      }, 1000 / 30)

      renderer.render(scene, camera)

      if (bodyTf.value) {
        const tf = bodyTf.value
        if (!initialRobotPositionOffset.value) {
          initialRobotPositionOffset.value = {
            y: tf.translation.z,
            x: tf.translation.x,
            z: -tf.translation.y
          }
        }
        robot.position.y = tf.translation.z - initialRobotPositionOffset.value.y + 0.1

        robot.position.x = tf.translation.x - initialRobotPositionOffset.value.x
        robot.position.z = -tf.translation.y - initialRobotPositionOffset.value.z

        const rotation = new THREE.Euler()
        rotation.setFromQuaternion(new THREE.Quaternion(tf.rotation.x, tf.rotation.y, tf.rotation.z, tf.rotation.w))
        robot.rotation.x = -rotation.y - Math.PI / 2
        robot.rotation.y = rotation.x
        robot.rotation.z = rotation.z

        if (robotJoints.value !== null) {
          const joints = robotJoints.value
          for (let j = 0; j < joints.position.length; j++) {
            robot.joints[joints.name[j]].setJointValue(joints.position[j])
          }
        }
      }
    }

    const sliderChooseFrame = (chosenFrameNum) => {
      frameNum.value = chosenFrameNum
    }

    const playFrame = () => {
      console.log(isPlaying.value)
      const frame = topicsData[frameNum.value]
      robotJoints.value = frame.robotJoints
      bodyTf.value = frame.bodyTf

      if (isPlaying.value === true) {
        if (frameNum.value < frameMax.value) {
          frameNum.value += 1
        }
      }
    }

    const loadRosbag = async () => {
      if (timerId.value) {
        clearInterval(timerId)
        frameMax.value = 0
        frameNum.value = 0
      }
      const bag = await open(file.value)
      const rosMessages = []
      let lastTopicFrame = {}

      await bag.readMessages({ topics: ['/tf', '/joint_states'] }, (result) => {
        rosMessages.push(result)

        if (result.topic === '/joint_states') {
          if (!lastTopicFrame.robotJoints) {
            lastTopicFrame.robotJoints = result.message
          }
        } else if (result.topic === '/tf') {
          if (result.message.transforms.length === 4) {
            result.message.transforms.forEach((transform) => {
              if (transform.child_frame_id === 'body') {
                if (!lastTopicFrame.bodyTf) {
                  lastTopicFrame.bodyTf = transform.transform
                }
              }
            })
          }
        }
        if (lastTopicFrame.bodyTf && lastTopicFrame.robotJoints) {
          topicsData.push(Object.assign({}, lastTopicFrame))
          lastTopicFrame = {}
        }
      })
      frameMax.value = topicsData.length
      console.log('Frames number', frameMax.value)
      timerId.value = setInterval(() => {
        playFrame()
      }, 40)
    }

    const onFileChanged = ($event) => {
      const target = $event.target
      if (target && target.files) {
        file.value = target.files[0]
        loadRosbag()
        console.log(file.value)
      }
    }

    onMounted(() => {
      stage.value.appendChild(renderer.domElement)
      animate()
    })

    return {
      scene,
      camera,
      renderer,
      light,
      axes,
      stage,
      status,
      onFileChanged,
      frameNum,
      frameMax,
      sliderChooseFrame,
      isPlaying,
      FRAME_WIDTH,
      FRAME_HEIGHT
    }
  }
})
</script>
