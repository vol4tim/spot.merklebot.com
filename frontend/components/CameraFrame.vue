<template>
  <div>
    <!--    <VideoContainer/>-->
    <!-- <img style="display: block;-webkit-user-select: none;margin: auto;background-color: hsl(0, 0%, 25%);" src="http://10.200.0.8:8000/video"> -->
    <img ref="image" class="w-full" style="display: block;-webkit-user-select: none;margin: auto;background-color: hsl(0, 0%, 25%);" src="https://api.merklebot.com/videoserver/video" @click="onClickImage">
  </div>
</template>

<script>
const calibrationNodes = [
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
    robot_x: -4,
    robot_y: 1.2,
    camera_x: 1095,
    camera_y: 609
  }
]

export default {
  name: 'CameraFrame',
  methods: {
    onClickImage (event) {
      const x = Math.floor(event.offsetX * (1280 / this.$refs.image.width))
      const y = Math.floor(event.offsetY * (720 / this.$refs.image.height))
      console.log(x, y)
      fetch('https://api.merklebot.com/strelka/go_to_point', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          camera_point_coords: [x, y],
          calibration_nodes: calibrationNodes
        })
      }).then(response => response.json()).then((data) => {

      })
    }
  }
}
</script>
