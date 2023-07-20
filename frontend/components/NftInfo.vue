<template>
  <div>
    <p class="text-md mt-2 text-white">
      <span class="text-yellow-500">{{ info.name }}</span>
    </p>

    <img :src="info.image" class="mt-2" style="width:200px">

    <p class="text-md mt-2 text-white" style="overflow: scroll;max-width: 550px;">
      {{ info.description }}
    </p>

    <p class="text-md mt-2 text-white">
      token: <a
        class="text-yellow-500"
        :href="`https://devnet.neonscan.org/address/${robot.cps.nft.contract}`"
        target="_blank"
        rel="noopener noreferrer"
      >{{ addressShort(robot.cps.nft.contract) }}</a>
    </p>
    <p class="text-md mt-2 text-white">
      tokenId: <span class="text-yellow-500">{{ robot.cps.nft.tokenId }}</span>
    </p>
  </div>
</template>

<script>
import { defineComponent } from '@nuxtjs/composition-api'
import { useRobot } from '../store/robot'

import { addressShort } from '~/plugins/robonomics'

export default defineComponent({
  props: {
    info: {
      type: Object,
      default: null
    }
  },
  setup () {
    const robot = useRobot()

    return {
      robot,
      addressShort
    }
  }
})
</script>
