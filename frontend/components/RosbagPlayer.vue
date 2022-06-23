<template>
  <div>
    <div ref="stage" class="stage" />
    <button
      type="button"
      class="uppercase py-2 my-2 px-4  bg-transparent dark:text-gray-800 dark:bg-white hover:dark:bg-gray-100 border-2 border-gray-800 text-gray-800 dark:text-white hover:bg-gray-800 hover:text-white text-md"
      @click="playBag"
    >
      Play bag
    </button>
  </div>
</template>

<script>
import * as THREE from 'three'
import TrackballControls from 'three-trackballcontrols'

import { LoaderUtils } from 'three'
import { XacroLoader } from 'xacro-parser'
import URDFLoader from 'urdf-loader'

import { defineComponent, ref, onMounted } from '@nuxtjs/composition-api'
import axios from 'axios'
import { open } from 'rosbag'

export default defineComponent({
  props: ['rosbagUrl'],
  setup (props) {
    const rosbagLink = props.rosbagUrl
    const stage = ref(null)
    const speed = ref(0.01)
    const initialRobotPositionOffset = ref(null)
    const robotJoints = ref([])
    const bagPlaying = ref(false)

    const url = '/urdf/spot.urdf.xacro'
    const xacroLoader = new XacroLoader()

    const scene = new THREE.Scene()
    const geometry = new THREE.PlaneGeometry(8, 8)
    const material = new THREE.MeshBasicMaterial({ color: '#BBBBBB', side: THREE.DoubleSide })
    const plane = new THREE.Mesh(geometry, material)

    const camera = new THREE.PerspectiveCamera(
      75,
      4 / 3,
      0.1,
      1000
    )
    const renderer = new THREE.WebGLRenderer({ antialias: true })
    const light = new THREE.DirectionalLight('hsl(0, 100%, 100%)')
    const axes = new THREE.AxesHelper(5)
    let robot = null

    camera.position.z = 0
    camera.position.y = 0.8
    camera.position.x = 1

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

      console.log('Robot parsed')
      console.log(robot.joints)
      robot.rotation.x = -Math.PI / 2
      scene.add(robot)
    })

    renderer.setSize(400, 300)
    light.position.set(5, 5, 0)

    scene.background = new THREE.Color('hsl(0, 100%, 100%)')

    const controls = new TrackballControls(camera, renderer.domElement)
    controls.rotateSpeed = 1.0
    controls.zoomSpeed = 5
    controls.panSpeed = 0.8
    controls.noZoom = false
    controls.noPan = false
    controls.staticMoving = true
    controls.dynamicDampingFactor = 0.3

    const curJointNum = ref(0)

    const animate = () => {
      // requestAnimationFrame(animate)
      // renderer.render(scene, camera)
      setTimeout(function () {
        requestAnimationFrame(animate)
      }, 1000 / 30)

      renderer.render(scene, camera)

      // cube.rotation.y += speed.value
      if (bagPlaying.value) {
        if (curJointNum.value > robotJoints.value.length - 1) {
          curJointNum.value = 0
          bagPlaying.value = false
        }

        const jointState = robotJoints.value[curJointNum.value][0]
        const tf = robotJoints.value[curJointNum.value][1]
        // console.log(tf.translation.z)
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
        // console.log(robot.position.y)

        const rotation = new THREE.Euler()
        rotation.setFromQuaternion(new THREE.Quaternion(tf.rotation.x, tf.rotation.y, tf.rotation.z, tf.rotation.w))
        console.log(tf.rotation)
        console.log(rotation)
        robot.rotation.x = -Math.PI / 2// rotation.z - Math.PI
        robot.rotation.x = rotation.z - Math.PI

        robot.rotation.y = -rotation.x
        robot.rotation.z = rotation.y
        console.log(robot.rotation.x)

        for (let j = 0; j < jointState.position.length; j++) {
          // console.log(jointState.name[j], jointState.position[j])
          robot.joints[jointState.name[j]].setJointValue(jointState.position[j])
        }
        curJointNum.value += 1
      }
      controls.update()
    }
    onMounted(() => {
      stage.value.appendChild(renderer.domElement)
      animate()
      console.log('ROSBAG LINK')
      console.log(rosbagLink)
    })

    const readBagFromUrl = async (rosbagUrl) => {
      const blobResponse = await axios({
        url: rosbagUrl,
        method: 'GET',
        responseType: 'blob'
      })
      console.log(blobResponse)
      const blobBag = new Blob([blobResponse.data])
      console.log(blobBag)
      const bag = await open(blobBag)
      console.log(bag)
      let prevTf = null
      await bag.readMessages({ topics: ['/tf', '/joint_states'] }, (result) => {
        // console.log(result.timestamp)
        console.log(result.message)
        if ((result.topic === '/tf') && (result.message.transforms.length === 4)) {
          result.message.transforms.forEach((transform) => {
            if (transform.child_frame_id === 'body') {
              prevTf = transform.transform
            }
          })
        } else if (result.topic === '/joint_states') {
          if (prevTf) {
            robotJoints.value.push([result.message, prevTf])
          }
          // console.log(result.message)
        }
      })
    }

    const playBag = async () => {
      console.log('Start playing rosbag')
      console.log(rosbagLink.value)
      await readBagFromUrl(rosbagLink)
      console.log(robotJoints.value)
      bagPlaying.value = true
    }

    return {
      scene,
      camera,
      controls: [],
      renderer,
      light,
      axes,
      speed,
      stage,
      playBag
    }
  }
})
</script>

<style scoped>

</style>
