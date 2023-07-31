<template>
  <div class="m-4 min-h-200 p-2">
    <div />

    <div class="mt-4">
      <CardContainer title="Saved data">
        <div v-if="robot.nftData!==null && robot.nftData.video">
          <div class="flex items-left justify-left m-4">
            <video :src="robot.nftData.video" type="video/mp4" controls />
          </div>
        </div>
        <div v-else>
          <p class="text-md mt-2 text-white">
            Your launch data will appear here after processing drawing and saving all data
          </p>
        </div>
      </CardContainer>

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
