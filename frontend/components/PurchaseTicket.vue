<template>
  <div>
    <div>
      <p class="text-md my-2 dark:text-white mx-6">
        One launch requires 1 ticket or 1 XRT.
      </p>
      <p class="text-md my-2 dark:text-white mx-6">
        You have:
      </p>
      <ul class="list-disc ml-8 text-md my-2 dark:text-white mx-6">
        <li>{{ wallet.selectedAccount.balanceFormatted }}</li>
        <li>{{ wallet.selectedAccount.tickets.filter(ticket=>ticket.spent===false).length }} tickets</li>
      </ul>
    </div>
    <div>
      <button
        type="button"
        class="h-12 w-120 py-2 px-4 my-4 items-center bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500 focus:ring-offset-indigo-200 text-white w-full transition ease-in duration-200 text-base font-semibold shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 rounded-lg"
        @click="checkout"
      >
        <span>Purchase a ticket for 5 USD</span>
        <img class="h-6 ml-2 inline-block bg-purple-600 rounded-lg" src="stripe.svg">
      </button>
    </div>
  </div>
</template>

<script>
import { defineComponent } from '@nuxtjs/composition-api'
import { useWallet } from '../store/wallet'
import { createSpotDemoTicketStripePurchaseSession } from '../plugins/merklebot'
import { getStripe } from '@/plugins/stripe'

export default defineComponent({
  setup () {
    const wallet = useWallet()

    const checkout = async () => {
      const stripeSessionId = await createSpotDemoTicketStripePurchaseSession(wallet.selectedAccount.account.address)
      const stripe = await getStripe()
      await stripe.redirectToCheckout({ sessionId: stripeSessionId })
    }

    return {
      wallet, checkout
    }
  }
})

</script>

<style scoped></style>
