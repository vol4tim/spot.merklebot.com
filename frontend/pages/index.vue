<template>
  <main class="bg-gray-800 font-mono">
    <div v-if="screenSize.w >= minScreenSize.w && screenSize.h >= minScreenSize.h" class="z-20 container mx-auto flex flex-row flex-wrap justify-center">
      <div class="basis-5/12">
        <AlwaysVisibleBlock />
      </div>

      <div class="basis-7/12">
        <ActivitiesBlock />
      </div>
    </div>
    <div v-else class="flex items-center justify-items-center w-full h-screen">
      <div class="container w-full max-h-fit text-center font-bold text-orange-600">
        Please open on a desktop computer in a window larger than {{ minScreenSize.w }} x {{ minScreenSize.h }}
      </div>
    </div>
  </main>
</template>

<script>
import { defineComponent, onMounted, ref, useRoute } from '@nuxtjs/composition-api'
import { useRobot } from '../store/robot'
import { useWallet } from '~/store/wallet'

export default defineComponent({
  setup () {
    const robot = useRobot()
    const wallet = useWallet()
    // wallet.connectWallet()

    const doRobotStatePolling = async () => {
      try {
        await robot.updateRobotState()
      } catch (e) {
        console.log('Spot state unavailable, retrying')
      }
      setTimeout(doRobotStatePolling, 1000)
    }
    const doTicketsListPolling = async () => {
      try {
        await wallet.updateTicketsList()
      } catch (e) {
        console.log('Can\'t update tickets list, retrying')
      }
      setTimeout(doTicketsListPolling, 1000)
    }

    const screenSize = ref({ w: window.innerWidth, h: window.innerHeight })

    onMounted(() => {
      document.documentElement.classList.add('dark')
      doRobotStatePolling()
      doTicketsListPolling()
      window.addEventListener('resize', () => {
        screenSize.value = { w: window.innerWidth, h: window.innerHeight }
      })

      // Scroll to 3-rd section after a Stripe purchase redirect.
      // Required while default browser behavior does not scroll to anchor inside a flexbox
      // as well as Element.scroll. Good for us anchor.click works.
      const route = useRoute()
      if (route.value.hash) {
        setTimeout(() => {
          document.getElementById(`anchor-to-${route.value.hash.slice(1)}`).click()
        }, 300)
      }
    })

    const minScreenSize = { w: 1000, h: 400 }

    return {
      screenSize, minScreenSize
    }
  }
})

</script>

<style scoped>
.screen {
  min-height: 80vh;
}
</style>
