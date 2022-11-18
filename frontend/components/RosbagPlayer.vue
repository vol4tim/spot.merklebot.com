<template>
  <div>
    <div>
      <input
        type="file"
        @change="onFileChanged($event)"
      >
    </div>
    <div>status: {{ status }}</div>
    <div ref="stage" class="stage" />
  </div>
</template>

<script>
import * as THREE from 'three'
import { LoaderUtils } from 'three'
import { XacroLoader } from 'xacro-parser'
import { open } from 'rosbag'
import URDFLoader from 'urdf-loader'
import { defineComponent, ref, onMounted } from '@nuxtjs/composition-api'

export default defineComponent({
  props: ['rosUrl', 'urdfUrl'],
  setup (props) {
    console.log(props)
    // const robotSocketLink = props.rosUrl
    const file = ref(null)
    const url = props.urdfUrl
    const status = ref('wait')
    const stage = ref(null)

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

    renderer.setSize(800, 500)
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

    const loadRosbag = async () => {
      const bag = await open(file.value)
      const rosMessages = []
      const topicsData = []
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
      for (let i = 0; i < topicsData.length; i++) {
        const frame = topicsData[i]
        setTimeout(() => {
          console.log(frame)
          robotJoints.value = frame.robotJoints
          bodyTf.value = frame.bodyTf
        }, i * 50)
      }
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

      // robotDataSocket.onopen = (e) => {
      //   console.log('Connection established')
      // }
      // robotDataSocket.onmessage = function (event) {
      //   const data = JSON.parse(event.data)
      //   console.log(data)
      //   const robotData = data.robot
      //   robotJoints.value = robotData.topics['/joint_states']
      //   const tfData = robotData.topics['/tf']
      //   if (tfData.transforms.length === 4) {
      //     tfData.transforms.forEach((transform) => {
      //       if (transform.child_frame_id === 'body') {
      //         bodyTf.value = transform.transform
      //       }
      //     })
      //   }
      // }
    })

    return {
      scene,
      camera,
      renderer,
      light,
      axes,
      stage,
      status,
      onFileChanged
    }
  }
})
</script>
