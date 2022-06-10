<template>
  <div>
    <div class="w-full mb-8">
      <canvas :id="canvasId" class="canvas-style" @mousedown="mouseDown" />
    </div>
    <div class="">
      <button
        type="button"
        class=" uppercase py-2 my-2 px-4  bg-transparent dark:text-gray-800 dark:bg-white hover:dark:bg-gray-100 border-2 border-gray-800 text-gray-800 dark:text-white hover:bg-gray-800 hover:text-white text-md"
        @click="resetCanvas"
      >
        Clear canvas
      </button>

      <button
        type="button"
        class=" uppercase py-2 my-2 px-4  bg-transparent dark:text-gray-800 dark:bg-white hover:dark:bg-gray-100 border-2 border-gray-800 text-gray-800 dark:text-white hover:bg-gray-800 hover:text-white text-md"
        @click="sendCommand"
      >
        Send command
      </button>
    </div>
  </div>
</template>

<script>
import { defineComponent, onMounted } from '@nuxtjs/composition-api'
import { useDashboardParameters } from '../store'
import { useRobot } from '../store/robot'

const paper = require('paper')

export default defineComponent({
  props: ['canvasId'],
  emits: ['drawing_sent'],
  setup (props, { emit }) {
    const robot = useRobot()
    let path = null
    let scope = null
    let paths = []
    const dashboardParameters = useDashboardParameters()

    onMounted(() => {
      scope = new paper.PaperScope()
      scope.setup(props.canvasId)
    })

    const resetCanvas = () => {
      dashboardParameters.setCodeSampleParameter(false)

      scope.project.activeLayer.removeChildren()
      paths = []
    }
    const sendCommand = async () => {
      const segments = []
      console.log('Sending command')
      console.log(paths)

      paths.forEach((path) => {
        const segment = []
        console.log(path._segments)
        path._segments.forEach((_segment) => {
          segment.push([_segment.point.x, _segment.point.y])
        })
        segments.push(segment)
      })
      console.log(segments)

      dashboardParameters.setCodeSampleParameter(true)
      const res = await robot.launchCps()
      if (res) {
        robot.sendDrawing(segments)
      }
      // fetch('http://10.200.0.3:1234/draw_figure', {

      // emit('drawing_sent', () => {
      //   fetch('https://api.merklebot.com/strelka/draw_figure', {
      //     method: 'POST',
      //     headers: {
      //       'Content-Type': 'application/json'
      //     },
      //     body: JSON.stringify({
      //       segments
      //     })
      //   }).then(response => response.json()).then((data) => {
      //     console.log(data)
      //   })
      // })
    }

    const pathCreate = (scope) => {
      scope.activate()
      return new paper.Path({
        strokeColor: '#000000',
        strokeJoin: 'round',
        strokeWidth: 1.5
      })
    }
    const createTool = (scope) => {
      console.log('createTool')
      scope.activate()
      return new paper.Tool()
    }

    const mouseDown = (ev) => {
      console.log('mouse down')
      // in order to access functions in nested tool
      // create drawing tool
      const tool = createTool(scope)
      tool.onMouseDown = (event) => {
        // init path
        path = pathCreate(scope)
        // add point to path
        path.add(event.point)
      }
      tool.onMouseDrag = (event) => {
        console.log('mouse drag')
        path.add(event)
      }
      tool.onMouseUp = (event) => {
        console.log('mouse up')
        // line completed
        path.add(event.point)
        path.simplify(10)
        path.flatten(3)
        paths.push({ ...path })
        console.log(paths)
      }
    }
    return {
      mouseDown, resetCanvas, sendCommand
    }
  }
})

</script>

<style scoped>
.canvas-style {
  cursor: crosshair;
  width: 100% !important;
  height: 300px !important;
  border: 2px solid black;
  border-radius: 0px;
  display: block;
  margin: auto;
}
</style>
