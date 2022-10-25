import axios from 'axios'

const client = axios.create({
  baseURL: 'https://api.merklebot.com'
})

/**
 * Read robonomics launch traces from backend by sender and launch tx nonce or launch tx id.
 * Check docs at https://api.merklebot.com/docs#/Robonomics-launch-traces/get_all_robonomics_launch_traces_get.
 * @param {string|null} [sender] - Sender's SS58 account address in Robonomics format.
 * @param {number|null} [nonce] - Launch tx nonce.
 * @param {string|null} [launchTxId] - Launch tx id.
 * @param {number|skip} [nonce] - Skip for getting all launches.
 * @param {number|limit} [nonce] - Limit for getting all launches.
 * @returns {?(Object|Array)} - All traces if no argument provided, traces related to the sender if specified, or a specific trace if launch tx nonce provided.
 */
export const readRobonomicsLaunchTracesBySender = async ({ sender = null, nonce = null, launchTxId = null, skip = 0, limit = 10_000 }) => {
  const resp = await client.get('robonomics-launch-traces', {
    params: {
      sender,
      nonce,
      skip,
      limit,
      launch_tx_id: launchTxId
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
  const resp = await client.post('spot-demo-ticket/checkout', {
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

export const retrieveFromFaucet = async (account, form) => {
  await client.post('faucet/retrieve', {
    account,
    form
  })
}

const versionsTime = {
  v1: {
    begin: 0,
    end: Date.parse('2022-08-22 16:41:19 +0000')
  },
  v2: {
    begin: Date.parse('2022-08-22 16:41:19 +0000') + 1, // first v2 record in database contains 2022-08-22T16:41:20
    end: Infinity
  }
}
const ipfsGatewayUrl = 'https://merklebot.mypinata.cloud/ipfs'

export const makeIpfsFolderLink = ({ ipfsCid, sender, nonce, createdAt }) => {
  const createdTime = Date.parse(createdAt + '+0000') // specify timezone, otherwise it takes local

  switch (true) {
    case (createdTime > versionsTime.v1.begin && createdTime < versionsTime.v1.end):
      // v1
      return `${ipfsGatewayUrl}/${ipfsCid}` +
             '/spot/spot.merklebot.com/spot/traces' +
             `/user-${sender}-cps-4FNQo2tK6PLeEhNEUuPePs8B8xKNwx15fX7tC2XnYpkC8W1j-session-${nonce}-${createdAt}`
    case (createdTime > versionsTime.v2.begin && createdTime < versionsTime.v2.end):
      // v2
      return `${ipfsGatewayUrl}/${ipfsCid}` +
             `/user-${sender}-cps-4FNQo2tK6PLeEhNEUuPePs8B8xKNwx15fX7tC2XnYpkC8W1j-session-${nonce}-${createdAt}`
    default:
      console.error({ msg: "can't identify version", createdAt, versionsTime })
  }
}

/**
 * Read NFT order.
 * @param {number} orderId
 * @returns {Object}
 */
export const readNftOrderById = async (orderId) => {
  const resp = await client.get(`spot-demo/nft/orders/${orderId}`)
  return resp.data
}
