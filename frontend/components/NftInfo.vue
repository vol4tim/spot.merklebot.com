<template>
  <div hidden>
    NFT Data: {{ nftOrderInfo }}
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
    const nftOrderInfo = props.data
    return { nftOrderInfo }
  }
})
</script>
