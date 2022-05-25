<template>
  <div style="position:relative;">
    <!--    <VideoContainer/>-->
    <!-- <img style="display: block;-webkit-user-select: none;margin: auto;background-color: hsl(0, 0%, 25%);" src="http://10.200.0.8:8000/video"> -->

    <img ref="image" class="w-full" style="display: block;-webkit-user-select: none;margin: auto;background-color: hsl(0, 0%, 25%);" src="https://api.merklebot.com/videoserver/video" @click="onClickImage">
    <div v-for="(pointer, index) in pointers" :key="index" class="clickEffect" :style="{'left': `${pointer[0]}px`, 'top': `${pointer[1]}px`}" />
    <div @click="startCalibration">
      Calibrate
    </div>
  </div>
</template>

<script>

export default {
  name: 'CameraFrame',
  data: () => {
    return {
      pointers: [],
      calibrationNodes: [
        {
          robot_x: 0,
          robot_y: 0,
          camera_x: 406,
          camera_y: 274
        },
        {
          robot_x: 0.7,
          robot_y: 1.5,
          camera_x: 19,
          camera_y: 322
        },
        {
          robot_x: 3,
          robot_y: -4.3,
          camera_x: 515,
          camera_y: 123
        },
        {
          robot_x: -2,
          robot_y: -5.2,
          camera_x: 1164,
          camera_y: 193
        },
        {
          robot_x: -3.97,
          robot_y: 1.2,
          camera_x: 1095,
          camera_y: 609
        }
      ],
      calibrationProcess: false,
      curCalibrationNodeIndex: 0

    }
  },
  methods: {
    startCalibration () {
      alert('Start calibration')
      this.calibrationProcess = true
      this.calibrationNodes = []
      this.curCalibrationNodeIndex = 0
    },
    onClickImage (event) {
      const x = Math.floor(event.offsetX * (1280 / this.$refs.image.width))
      const y = Math.floor(event.offsetY * (720 / this.$refs.image.height))
      console.log(x, y)
      this.pointers.push([event.clientX, event.clientY])
      // pointer.style.top = event.clientY + 'px'
      // pointer.style.left = event.clientX + 'px'
      if (this.calibrationProcess) {
        // this.calibrationNodes[this.curCalibrationNodeIndex].camera_x = x
        // this.calibrationNodes[this.curCalibrationNodeIndex].camera_y = x

        const _node = {
          robot_x: 0,
          robot_y: 0,
          camera_x: 0,
          camera_y: 0
        }

        fetch('https://api.merklebot.com/strelka/odom', {
          method: 'GET'
        }).then(response => response.json()).then((data) => {
          _node.robot_x = data.position.x
          _node.robot_y = data.position.y
        })

        _node.camera_x = x
        _node.camera_y = y

        this.calibrationNodes.push(_node)

        this.curCalibrationNodeIndex += 1
        if (this.curCalibrationNodeIndex >= 16) {
          this.calibrationProcess = false
          fetch('https://api.merklebot.com/strelka/set_movement_calibration_nodes', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              calibration_nodes: this.calibrationNodes
            })
          }).then(response => response.json()).then((data) => {

          })

          alert('Calibration finished')
        }
      } else {
        fetch('https://api.merklebot.com/strelka/go_to_point', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            camera_point_coords: [x, y],
            calibration_nodes: this.calibrationNodes
          })
        }).then(response => response.json()).then((data) => {

        })
      }
    }

  }
}
</script>

<style>
div.clickEffect{
  position:fixed;
  box-sizing:border-box;
  border-style:solid;
  border-color: #8ed080;
  border-radius:50%;
  animation:clickEffect 0.4s ease-out;
  z-index:99999;
}
@keyframes clickEffect{
  0%{
    opacity:1;
    width:0.5em; height:0.5em;
    margin:-0.25em;
    border-width:0.5em;
  }
  100%{
    opacity:0.2;
    width:8em; height:7em;
    margin:-4em;
    border-width:0.03em;
  }
}

</style>
