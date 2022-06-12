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
        :disabled="!hasEnoughXrt"
        @click="sendCommandXrt"
      >
        Launch for 1 XRT
      </button>

      <button
        type="button"
        class=" uppercase py-2 my-2 px-4  bg-transparent dark:text-gray-800 dark:bg-white hover:dark:bg-gray-100 border-2 border-gray-800 text-gray-800 dark:text-white hover:bg-gray-800 hover:text-white text-md"
        :disabled="!hasTicket"
        @click="sendCommandTicket"
      >
        Launch for 1 ticket
      </button>
    </div>
  </div>
</template>

<script>
import { defineComponent, onMounted, computed } from '@nuxtjs/composition-api'
import { useDashboardParameters } from '../store'
import { useRobot } from '../store/robot'
import { useWallet } from '../store/wallet'

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

    const sendCommand = async (transferXrtAmount) => {
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
      try {
        const res = await robot.launchCps(transferXrtAmount)
        const paymentMode = transferXrtAmount ? 'xrt' : 'ticket'
        if (res) {
          robot.sendDrawing(segments, paymentMode, `${res.txInfo.blockNumber}-${res.txInfo.txIndex}`)
        }
      } catch (e) {
        console.error(e)
      }
    }

    const sendCommandXrt = async () => {
      await sendCommand(1 * 10 ** 9) // 1 Wn, 1 Wn = 1 * 10 ^ -9 XRT
    }

    const sendCommandTicket = async () => {
      await sendCommand()
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

    const wallet = useWallet()

    const hasEnoughXrt = computed(() => {
      return wallet.selectedAccount.balanceRaw * 10 ** -9 > 1
    })

    const hasTicket = computed(() => {
      return wallet.selectedAccount.tickets.filter(ticket => ticket.spent === false).length >= 1
    })

    return {
      mouseDown, resetCanvas, sendCommandXrt, sendCommandTicket, hasEnoughXrt, hasTicket
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
