import axios from 'axios'

const client = axios.create({
  baseURL: 'https://api.merklebot.com'
})

/**
 * Read robonomics launch traces from backend by sender and launch tx nonce.
 * Check docs at https://api.merklebot.com/docs#/Robonomics-launch-traces/get_all_robonomics_launch_traces_get.
 * @param {string} [sender] - Sender's SS58 account address in Robonomics format.
 * @param {number} [nonce] - Launch tx nonce.
 * @returns {?(Object|Array)} - All traces if no argument provided, traces related to the sender if specified, or a specific trace if launch tx nonce provided.
 */
export const readRobonomicsLaunchTracesBySender = async (sender, nonce) => {
  const resp = await client.get('robonomics-launch-traces', {
    params: {
      sender,
      nonce
    }
  })
  return resp.data
}

/**
 * Create new Stripe payment session to purchase Spot demo ticket by card.
 * @param {string} customer - Customer's account address to receive purchased ticket. Robonomics parachain format expected.
 * @returns {string} - Stripe payment session id to use for redirection.
 */
export const createSpotDemoTicketStripePurchaseSession = async (customer) => {
  const resp = await client.post('ticket/checkout', {
    quantity: '1',
    account: customer
  })
  return resp.data.id
}

/**
 * Read customer's tickets.
 * @param {string} customer - Customer's account address. Robonomics parachain format expected.
 * @param {boolean} [spent] - Returns all if not specified, otherwise returns spent or unspent tickets only.
 * @returns {Array} - Customer's tickets.
 */
export const readTicketsByCustomer = async (customer, spent) => {
  const resp = await client.get('spot-demo/tickets', {
    params: {
      customer,
      spent
    }
  })
  return resp.data
}

/**
 * Spend ticket with an id specified.
 * @param {string} ticketId - Id of the ticket to spend.
 */
export const createTicketSpending = async (ticketId) => {
  await client.post('spot-demo/spendings', {
    params: {
      ticket_id: ticketId
    }
  })
}
