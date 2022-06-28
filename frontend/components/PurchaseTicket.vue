<template>
  <div class="w-full">
    <p class="text-md my-2 text-white">
      One launch requires 1 ticket <em>or</em> 1 XRT.
    </p>
    <div class="">
      <PayWithToggle>
        <template #ticket>
          <div class="w-full px-2 bg-gray-600 relative">
            <p class="text-md my-4 mb-16 text-white text-center">
              You have {{
                wallet.selectedAccount.tickets.filter(
                  (ticket) => ticket.spent === false
                ).length
              }}
              tickets
            </p>
            <button
              type="button"
              class="absolute bottom-0 inset-x-0 uppercase py-2 mx-4 my-2 px-4 md:mt-16 bg-gray-200 border-2
                     hover:bg-gray-300 hover:bg-gray-800 hover:text-white text-md text-center"
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
              class="absolute bottom-0 inset-x-0 uppercase py-2 mx-4 my-2 px-4 md:mt-16 bg-white border-2
                     hover:bg-gray-300 hover:bg-gray-800 hover:text-white text-md text-center"
            >
              Get XRT
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
