<template>
  <UserInfoSurvey @submit="onServeyComplete" />
</template>

<script>
import { defineComponent } from '@nuxtjs/composition-api'
import { useWallet } from '~/store/wallet'
import { retrieveFromFaucet } from '~/plugins/merklebot'

export default defineComponent({
  emits: ['complete'],
  setup (props, { emit }) {
    const wallet = useWallet()

    const onServeyComplete = async (data) => {
      console.log('Survey completed')
      await retrieveFromFaucet(wallet.selectedAccount.account.address, data)
      emit('complete')
    }
    return { onServeyComplete }
  }
})
</script>
