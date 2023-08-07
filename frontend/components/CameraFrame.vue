<template>
  <div style="position:relative;">
    <!--    <VideoContainer/>-->
    <!-- <img style="display: block;-webkit-user-select: none;margin: auto;background-color: hsl(0, 0%, 25%);" src="http://10.200.0.8:8000/video"> -->

    <!--    <img-->
    <!--      v-if="imageLoaded"-->
    <!--      ref="image"-->
    <!--      class="w-full"-->
    <!--      style="display: block;-webkit-user-select: none;margin: auto;background-color: hsl(0, 0%, 25%);"-->
    <!--      src="https://api.merklebot.com/videoserver/video"-->
    <!--      :style="interactionMode==='drawing'?{'aspect-ratio': '4/3', 'object-fit': 'cover'}:{}"-->
    <!--      @click="onClickImage"-->
    <!--      @error="onImageError"-->
    <!--    >-->
    <div>
      <!-- <iframe
        style="display: block;-webkit-user-select: none;margin: auto;background-color: hsl(0, 0%, 25%);"
        src="https://player.twitch.tv/?channel=merklebotStreamer&amp;parent=vol4tim.github.io"
        frameborder="0"
        allowfullscreen="true"
        scrolling="no"
        height="350"
        class="w-full"
      /> -->

      <iframe
        width="100%"
        height="315"
        src="https://www.youtube.com/embed/6NSKCqg0g7k"
        title="YouTube video player"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        allowfullscreen
      />
    </div>
    <p v-if="!imageLoaded" class="text-3xl my-6 text-center text-red-600">
      Camera isn't loaded
    </p>
    <div v-for="(pointer, index) in pointers" :key="index" class="clickEffect" :style="{'left': `${pointer[0]}px`, 'top': `${pointer[1]}px`}" />
    <div v-if="interactionMode==='movement'" @click="startCalibration">
      Calibrate
    </div>
  </div>
</template>

<script>

export default {
  name: 'CameraFrame',
  props: ['interactionMode'],
  data: () => {
    return {
      pointers: [],
      calibrationNodes: [],
      calibrationProcess: false,
      curCalibrationNodeIndex: 0,
      imageLoaded: true

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
      if (this.interactionMode !== 'movement') {
        return
      }
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
    },
    onImageError () {
      this.imageLoaded = false
      console.log('camera image error')
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
