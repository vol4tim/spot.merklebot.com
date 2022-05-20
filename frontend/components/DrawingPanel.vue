<template>
  <div>
    <div class="w-full mb-8">
      <canvas :id="canvasId" class="canvas-style" @mousedown="mouseDown" />
    </div>
    <button
      type="button"
      class="py-2 px-4 mt-2 bg-indigo-500 hover:bg-indigo-600 focus:ring-indigo-400 focus:ring-offset-indigo-200 text-white w-full transition ease-in duration-200 text-center text-base font-semibold shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2  rounded-lg "
      @click="resetCanvas"
    >
      Reset
    </button>

    <button
      type="button"
      class="py-2 px-4 mt-4 bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500 focus:ring-offset-indigo-200 text-white w-full transition ease-in duration-200 text-center text-base font-semibold shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2  rounded-lg "
      @click="sendCommand"
    >
      Send Command
    </button>
  </div>
</template>

<script>
const paper = require('paper')
export default {
  name: 'DrawingPanel',
  props: ['canvasId'],
  data: () => {
    return {
      path: null,
      scope: null,
      paths: []
    }
  },
  mounted () {
    this.scope = new paper.PaperScope()
    this.scope.setup(this.canvasId)
  },
  methods: {
    resetCanvas () {
      this.scope.project.activeLayer.removeChildren()
      this.paths = []
    },
    sendCommand () {
      const segments = []
      console.log('Sending command')
      console.log(this.paths)

      this.paths.forEach((path) => {
        const segment = []
        console.log(path._segments)
        path._segments.forEach((_segment) => {
          segment.push([_segment.point.x, _segment.point.y])
        })
        segments.push(segment)
      })
      console.log(segments)
      // fetch('http://10.200.0.3:1234/draw_figure', {
      fetch('https://api.merklebot.com/strelka/draw_figure', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          segments
        })
      }).then(response => response.json()).then((data) => {
        this.$emit('drawing_sent')
        console.log(data)
      })
    },
    pathCreate (scope) {
      scope.activate()
      return new paper.Path({
        strokeColor: '#000000',
        strokeJoin: 'round',
        strokeWidth: 1.5
      })
    },
    createTool (scope) {
      console.log('createTool')
      scope.activate()
      return new paper.Tool()
    },
    mouseDown (ev) {
      console.log('mouse down')
      // in order to access functions in nested tool
      const self = this
      // create drawing tool
      this.tool = this.createTool(this.scope)
      this.tool.onMouseDown = (event) => {
        // init path
        self.path = self.pathCreate(self.scope)
        // add point to path
        self.path.add(event.point)
      }
      this.tool.onMouseDrag = (event) => {
        console.log('mouse drag')
        self.path.add(event)
      }
      this.tool.onMouseUp = (event) => {
        console.log('mouse up')
        // line completed
        self.path.add(event.point)
        self.path.simplify(10)
        self.path.flatten(10)
        self.paths.push({ ...self.path })
        console.log(self.paths)
      }
    }
  }
}
</script>

<style scoped>
.canvas-style {
  cursor: crosshair;
  width: 100% !important;
  height: 300px !important;
  border: 5px solid black;
  border-radius: 10px;
  display: block;
  margin: auto;
  box-shadow: 0 10px 8px -8px black;
}
</style>
