<template>
  <div class="m-4 min-h-200 p-2">
    <div />

    <div class="mt-4">
      <CardContainer class="mt-8" title="NFT data">
        <NftInfo v-if="robot.nftData!==null" :info="robot.nftData" />
        <div v-else>
          <p class="text-md mt-2 text-white">
            Your NFT data will appear here after minting.
          </p>
        </div>
      </CardContainer>
    </div>
  </div>
</template>
<script>
import { defineComponent } from '@nuxtjs/composition-api'
import { useRobot } from '../store/robot'

export default defineComponent({
  setup () {
    const robot = useRobot()

    return {
      robot
    }
  }
})
</script>
