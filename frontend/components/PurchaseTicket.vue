<template>
  <div>
    <div>
      <h3>One launch requires 1 ticket or 1 XRT</h3>
      <h3>You have:</h3>
      <ul class="list-disc ml-8">
        <li>{{ xrtBalance }} XRT</li>
        <li>{{ ticketsBalance }} tickets</li>
      </ul>
    </div>
    <div>
      <button
        type="button"
        class="py-2 px-4 mt-4 bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500 focus:ring-offset-indigo-200 text-white w-full transition ease-in duration-200 text-center text-base font-semibold shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 rounded-lg"
        @click="checkout"
      >
        Purchase a ticket for 5 USD
        <img class="stripe" alt="" src="stripe.svg">
      </button>
    </div>
  </div>
</template>

<script>
import {
  createSpotDemoTicketStripePurchaseSession
} from '@/plugins/merklebot'
import { getStripe } from '@/plugins/stripe'

export default {
  name: 'PurchaseTicket',
  props: {
    xrtBalance: {
      type: Number,
      default: null
    },
    ticketsBalance: {
      type: Number,
      default: null
    },
    address: {
      type: String,
      default: null
    }
  },
  methods: {
    async checkout () {
      const stripeSessionId = await createSpotDemoTicketStripePurchaseSession(this.address)
      const stripe = await getStripe()
      await stripe.redirectToCheckout({ sessionId: stripeSessionId })
    }
  }
}
</script>

<style scoped></style>
