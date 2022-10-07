<template>
  <div>
    <div>status: {{ status }}</div>
    <div ref="stage" class="stage" />
  </div>
</template>

<script>
import * as THREE from 'three'
import TrackballControls from 'three-trackballcontrols'

import { LoaderUtils } from 'three'
import { XacroLoader } from 'xacro-parser'
import URDFLoader from 'urdf-loader'

import { defineComponent, ref, onMounted } from '@nuxtjs/composition-api'
// import ROSLIB from 'roslib'
// import sha512 from 'crypto-js/sha512'
// import UAParser from 'ua-parser-js'
// const client = new UAParser()

export default defineComponent({
  props: ['rosUrl', 'urdfUrl'],
  setup (props) {
    console.log(props)
    const robotSocketLink = props.rosUrl
    const url = props.urdfUrl
    const status = ref('wait')
    const stage = ref(null)

    const initialRobotPositionOffset = ref(null)
    const bodyTf = ref(null)
    const robotJoints = ref(null)
    const xacroLoader = new XacroLoader()

    // const ros = new ROSLIB.Ros({
    //   url: robotSocketLink
    // })
    const robotDataSocket = new WebSocket(robotSocketLink)

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

      robot.rotation.x = -Math.PI / 2
      scene.add(robot)
      status.value = 'urdf loaded'
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
        robot.rotation.x = rotation.y - Math.PI / 2
        robot.rotation.y = rotation.x
        robot.rotation.z = rotation.z + Math.PI / 2

        if (robotJoints.value !== null) {
          const joints = robotJoints.value
          for (let j = 0; j < joints.position.length; j++) {
            robot.joints[joints.name[j]].setJointValue(joints.position[j])
          }
        }
      }

      controls.update()
    }
    onMounted(() => {
      stage.value.appendChild(renderer.domElement)
      animate()
      robotDataSocket.onopen = (e) => {
        console.log('Connection established')
      }
      robotDataSocket.onmessage = function (event) {
        const data = JSON.parse(event.data)
        console.log(data)
        const robotData = data.robot
        robotJoints.value = robotData.topics['/joint_states']
        const tfData = robotData.topics['/tf']
        if (tfData.transforms.length === 4) {
          tfData.transforms.forEach((transform) => {
            if (transform.child_frame_id === 'body') {
              bodyTf.value = transform.transform
            }
          })
        }
      }
    })
    // connectRos(){
    // const secret = '1234567880abcdef'
    // const dest = robotSocketLink
    // const rand = (Math.random() + 1).toString(36).substring(10)
    // const time = new Date().getTime() / 1000
    // const timeEnd = time + 1000
    // const level = 'admin'
    // const mac = sha512(secret + client.getUA() + dest + rand + parseInt(time).toString() + level + parseInt(timeEnd).toString()) // using sha512 library js-sha512 and client library clientjs
    // ros.authenticate(mac, client.getUA(), dest, rand, time, level, timeEnd) // method from roslibjs
    //
    // ros.on('connection', () => {
    //   status.value = 'connected'
    //   const tfTopic = new ROSLIB.Topic({
    //     ros,
    //     name: '/tf',
    //     messageType: 'tf2_msgs/TFMessage'
    //   })
    //   tfTopic.subscribe((message) => {
    //     if (message.transforms.length === 4) {
    //       message.transforms.forEach((transform) => {
    //         if (transform.child_frame_id === 'body') {
    //           bodyTf.value = transform.transform
    //         }
    //       })
    //     }
    //   })
    //
    //   const jointsTopic = new ROSLIB.Topic({
    //     ros,
    //     name: '/joint_states',
    //     messageType: 'sensor_msgs/JointState'
    //   })
    //   jointsTopic.subscribe((message) => {
    //     robotJoints.value = message
    //   })
    // })
    // ros.on('error', (e) => {
    //   console.log(e)
    // })
    // }

    return {
      scene,
      camera,
      renderer,
      light,
      axes,
      stage,
      status
    }
  }
})
</script>
