<template>
  <div class="w-full">
    <p class="text-md my-2 text-white">
      One launch requires 1 ticket <em>or</em> 1 XRT.
    </p>
    <div>
      <PayWithToggle>
        <template #ticket>
          <div class="w-full px-2 bg-gray-600 relative">
            <p class="text-md my-4 mb-2 text-white text-center">
              You have {{
                wallet.selectedAccount.tickets.filter(
                  (ticket) => ticket.spent === false
                ).length
              }}
              tickets
            </p>
            <button
              type="button"
              class="uppercase text-md w-full py-2 my-2 px-4 bg-gray-200 text-gray-800
                hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
              @click="checkout"
            >
              <span>Get ticket</span>
              <img
                class="h-6 ml-2 inline-block bg-indigo-400 rounded-lg"
                src="stripe.svg"
              >
            </button>
          </div>
        </template>
        <template #XRT>
          <div class="w-full px-2 bg-gray-600 relative">
            <p class="text-md my-4 mb-16 text-white text-center">
              You have {{ wallet.selectedAccount.balanceFormatted }}
            </p>
            <a
              href="https://www.kraken.com/prices/xrt-robonomics-price-chart/usd-us-dollar?interval=1m"
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
import { defineComponent, computed } from '@nuxtjs/composition-api'
import { useWallet } from '../store/wallet'
import { createSpotDemoTicketStripePurchaseSession } from '../plugins/merklebot'
import { getStripe } from '@/plugins/stripe'

export default defineComponent({
  setup () {
    const wallet = useWallet()

    const checkout = async () => {
      const stripeSessionId = await createSpotDemoTicketStripePurchaseSession(
        wallet.selectedAccount.account.address
      )
      const stripe = await getStripe()
      await stripe.redirectToCheckout({ sessionId: stripeSessionId })
    }

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
      checkout,
      hasEnoughXrt,
      hasTicket
    }
  }
})
</script>

<style scoped></style>
