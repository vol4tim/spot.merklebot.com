<template>
  <div class="w-full">
    <div>
      <PayWithToggle>
        <template #XRT>
          <div class="w-full px-2 bg-gray-600 relative">
            <p class="text-md my-4 mb-16 text-white text-center">
              You have {{ wallet.selectedAccount.balanceFormatted }}
            </p>
            <a
              href="https://discord.gg/mAD3aWaX"
              target="_blank"
              rel="noopener noreferrer"
              class="absolute bottom-0 inset-x-0 uppercase py-2 my-2 mx-2 px-2 bg-gray-200 text-gray-800
                text-md text-center hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
            >
              <span>Get XRT</span>
            </a>
          </div>
        </template>
      </PayWithToggle>
    </div>
    <span
      v-if="hasTicket || hasEnoughXrt"
      class="text-md my-2 text-white"
    >
      It is enough to launch the robot by
      <span v-if="hasTicket"> ticket</span>
      <span v-if="hasTicket && hasEnoughXrt"> or</span>
      <span v-if="hasEnoughXrt"> XRT</span>.
    </span>
    <span v-else class="text-md my-2 text-white">
      It is not enough to launch the robot. Purchase a ticket <em>or</em> get
      XRT.
    </span>
  </div>
</template>

<script>
import { computed, defineComponent } from '@nuxtjs/composition-api'
import { useWallet } from '../store/wallet'

export default defineComponent({
  setup () {
    const wallet = useWallet()

    const hasEnoughXrt = computed(() => {
      return wallet.selectedAccount.balanceRaw * 10 ** -9 > 1
    })

    const hasTicket = computed(() => {
      return (
        wallet.selectedAccount.tickets.filter(
          ticket => ticket.spent === false
        ).length >= 1
      )
    })

    return {
      wallet,
      hasEnoughXrt,
      hasTicket
    }
  }
})
</script>

<style scoped></style>
