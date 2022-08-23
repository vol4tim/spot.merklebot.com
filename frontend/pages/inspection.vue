<template>
  <main class="bg-gray-800 font-mono">
    <div class="z-20 container mx-auto flex flex-row flex-wrap justify-center">
      <div class="basis-5/12">
        <InspectionRobotStatePanel />
      </div>

      <div class="basis-7/12">
        <InspectionControlsBlock />
      </div>
    </div>
  </main>
</template>

<script>
import { defineComponent, onMounted } from '@nuxtjs/composition-api'
import { useRobot } from '../store/robot'
import { useWallet } from '~/store/wallet'
import { useSpot } from '~/store/spot'

export default defineComponent({
  setup () {
    const robot = useRobot()
    const wallet = useWallet()
    const spot = useSpot()

    const connectToSpot = () => {
      try {
        const spotSocket = new WebSocket('wss://api.merklebot.com/oz/spot/spot/state/ws')
        spotSocket.onmessage = (event) => {
          spot.setSpotAnswer(JSON.parse(event.data))
        }
        spotSocket.onopen = () => spot.setStatus('connected')
        spotSocket.onclose = () => {
          spot.setSpotAnswer()
          setTimeout(connectToSpot, 1000)
        }
        spotSocket.onerror = () => spotSocket.close()
      } catch {
        setTimeout(connectToSpot, 1000)
      }
    }

    const doTicketsListPolling = async () => {
      try {
        await wallet.updateTicketsList()
      } catch (e) {
        console.log('Can\'t update tickets list, retrying')
      }
      setTimeout(doTicketsListPolling, 1000)
    }

    const doRobotStatePolling = async () => {
      try {
        await robot.updateRobotState()
      } catch (e) {
        console.log('Spot state unavailable, retrying')
      }
      setTimeout(doRobotStatePolling, 1000)
    }

    onMounted(() => {
      doRobotStatePolling()
      doTicketsListPolling()
      connectToSpot()
    })

    return {
    }
  }
})

</script>

<style scoped>
.screen {
  min-height: 80vh;
}
</style>
