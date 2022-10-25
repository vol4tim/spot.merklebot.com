<template>
  <div hidden>
    NFT Data: {{ nftOrderInfo }}
    <p class="text-md mt-2 text-white">
      NFT minting status:
      <span v-if="nftOrderInfo" class="text-yellow-500">{{ nftOrderInfo.status }}</span>
      <Spinner v-else />
    </p>
    <p v-if="['minted', 'delivered'].includes(nftOrderInfo.status)" class="text-md mt-2 text-white">
      Find your NFT at:
    </p>
  </div>
</template>

<script>
import { defineComponent } from '@vue/composition-api'

export default defineComponent({
  props: {
    info: {
      type: Object,
      default: null
    }
  },
  setup (props) {
    const nftOrderInfo = props.info

    const makeNftUrl = (collectionId, symbol, mintBlock, serialNumber) => {
      return `https://singular.app/collectibles/kusama/${collectionId}-${symbol}/${mintBlock}-${collectionId}-${symbol}-${symbol}-${serialNumber}`
    }

    return { nftOrderInfo, makeNftUrl }
  }
})
</script>
