<template>
  <div>
    <span>
      {{
        account === null
          ? "-"
          : account
            ? `${account.substring(0, 6)}...${account.substring(
              account.length - 4
            )}`
            : ""
      }}
    </span>
  </div>
</template>

<script>
import { useWeb3 } from '@instadapp/vue-web3'
import { defineComponent } from '@nuxtjs/composition-api'

export default defineComponent({
  setup () {
    const { account } = useWeb3()

    return { account }
  }
})
</script>
