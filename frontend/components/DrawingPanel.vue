<template>
  <div>
    <div class="w-full mb-8">
      <canvas :id="canvasId" class="canvas-style" @mousedown="mouseDown" />
    </div>
    <button
      type="button"
      class="
      uppercase text-md w-full py-2 my-2 px-4
        bg-gray-200 text-gray-800 hover:bg-gray-800 hover:bg-gray-100 hover:text-white
      "
      @click="resetCanvas"
    >
      Clear canvas
    </button>
  </div>
</template>

<script>
import { defineComponent, onMounted } from '@nuxtjs/composition-api'
import { useDashboardParameters, useDAppParameters } from '../store'
const paper = require('paper')

export default defineComponent({
  props: ['canvasId'],
  emits: ['drawing_sent'],
  setup (props, { emit }) {
    let path = null
    let scope = null
    let paths = []
    const dashboardParameters = useDashboardParameters()
    const dAppParameters = useDAppParameters()

    onMounted(() => {
      scope = new paper.PaperScope()
      scope.setup(props.canvasId)
    })

    const updateDrawingSegments = () => {
      dAppParameters.currentDrawingSegments = []
      paths.forEach((path) => {
        const segment = []
        console.log(path._segments)
        path._segments.forEach((_segment) => {
          segment.push([_segment.point.x, _segment.point.y])
        })
        dAppParameters.currentDrawingSegments.push(segment)
      })
    }

    const resetCanvas = () => {
      dashboardParameters.setCodeSampleParameter(false)

      scope.project.activeLayer.removeChildren()
      paths = []
      updateDrawingSegments()
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
        updateDrawingSegments()
      }
    }

    return {
      mouseDown, resetCanvas
    }
  }
})

</script>

<style scoped>
.canvas-style {
  cursor: crosshair;
  width: 100% !important;
  height: 300px !important;
  display: block;
  margin: auto;
  background-color: rgb(255 237 213); /* tailwindcss orange-100 */
}
</style>
