<template>
  <main class="bg-gray-800 font-mono">
    <div
      v-if="screenSize.w >= minScreenSize.w && screenSize.h >= minScreenSize.h"
      class="z-20 container mx-auto flex flex-row flex-wrap justify-center"
    >
      <div class="basis-5/12">
        <div class="px-6 py-4 sticky top-0">
          <AlwaysVisibleBlock />
        </div>
      </div>

      <div class="basis-7/12">
        <ActivitiesBlock />
      </div>
    </div>
    <div v-else class="items-center justify-items-center w-full h-screen">
      <div>
        <AlwaysVisibleBlock />
      </div>
      <div>
        <ActivitiesBlock />
      </div>
    </div>
  </main>
</template>

<script>
import { defineComponent, onMounted, ref, useRoute, watch } from '@nuxtjs/composition-api'
import { topic } from '../connectors/config'
import { useRobot } from '../store/robot'

import { useIpfs } from '~/plugins/ipfs'
import { useWallet } from '~/store/wallet'

export default defineComponent({
  setup () {
    const robot = useRobot()
    const wallet = useWallet()
    wallet.connectWallet()

    const { ipfs } = useIpfs()
    watch([ipfs], () => {
      if (ipfs.value) {
        ipfs.value.pubsub.subscribe(topic, (r) => {}, { discover: true })
        setInterval(() => {
          ipfs.value.pubsub.peers(topic).then((peers) => {
            console.log('ipfs pubsub peers', peers)
          })
        }, 10000)
      }
    })

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
