<template>
  <div>
    <p class="text-md mt-2 text-white">
      Status: <span class="text-yellow-500">{{ robot.nftData.status }}</span>
    </p>

    <img :src="nftOrderInfo.image_url" class="mt-2">

    <p class="text-md mt-2 text-white">
      NFT Link: <a
        v-if="['minted', 'delivered'].includes(robot.nftData.status)"
        :href="makeNftUrl('b437f70371c8622e02', 'MBVD-2023', robot.nftData.nft_mint_block_number, robot.nftData.nft_serial_num)"
        class="text-yellow-500"
        target="_blank"
        rel="noopener noreferrer"
      >View in Singular</a>
      <Spinner v-else />
    </p>
  </div>
</template>

<script>
import { defineComponent } from '@vue/composition-api'
import { useRobot } from '~/store/robot'

export default defineComponent({
  props: {
    info: {
      type: Object,
      default: null
    }
  },
  setup (props) {
    const nftOrderInfo = props.info
    const robot = useRobot()

    const makeNftUrl = (collectionId, symbol, mintBlock, serialNumber) => {
      const nftSerialNumber = `${serialNumber}`.padStart(8, '0')
      return `https://singular.app/collectibles/kusama/${collectionId}-${symbol}/${mintBlock}-${collectionId}-${symbol}-${symbol}-${nftSerialNumber}`
    }

    console.log('Nft Order info')
    console.log(nftOrderInfo)
    return { nftOrderInfo, makeNftUrl, robot }
  }
})
</script>
