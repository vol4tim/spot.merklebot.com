<template>
  <div>
    <div class="w-full mb-8">
      <canvas :id="canvasId" class="canvas-style" @mousedown="mouseDown" />
    </div>
    <button
      type="button"
      class="
        uppercase text-md w-full py-2 my-2 px-4
        bg-gray-200 hover:bg-gray-300 hover:text-white
      "
      @click="resetCanvas"
    >
      Clear canvas
    </button>

    <PayWithToggle>
      <template #ticket>
        <div class="w-full px-2 bg-gray-600 relative">
          <p class="text-md my-4 mb-16 text-white text-center">
            You have {{
              wallet.selectedAccount.tickets.filter(
                (ticket) => ticket.spent === false
              ).length
            }}
            tickets
          </p>
          <button
            type="button"
            class="
              absolute bottom-0 inset-x-0 uppercase py-2 mx-4 my-2 px-4 md:mt-16
              text-md text-center
              text-gray-800 bg-gray-200 border-2
              hover:bg-gray-100 hover:bg-gray-800 hover:text-white
            "
            :disabled="!hasTicket"
            @click="sendCommandTicket"
          >
            Launch for 1 ticket
          </button>
        </div>
      </template>
      <template #XRT>
        <div class="w-full px-2 bg-gray-600 relative">
          <p class="text-md my-4 mb-16 text-white text-center">
            You have {{ wallet.selectedAccount.balanceFormatted }}
          </p>

          <button
            type="button"
            class="
              absolute bottom-0 inset-x-0 uppercase py-2 mx-4 my-2 px-4 md:mt-16
              text-md text-center
              text-gray-800 bg-gray-200 border-2
              hover:bg-gray-100 hover:bg-gray-800 hover:text-white
            "
            :disabled="!hasEnoughXrt"
            @click="sendCommandXrt"
          >
            Launch for 1 XRT
          </button>
        </div>
      </template>
    </PayWithToggle>
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
      mouseDown, resetCanvas, sendCommandXrt, sendCommandTicket, hasEnoughXrt, hasTicket, wallet
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
