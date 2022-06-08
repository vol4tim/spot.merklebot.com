import { loadStripe } from '@stripe/stripe-js'

let stripe

export const getStripe = async () => {
  if (stripe) { return stripe }
  stripe = await loadStripe(
    'pk_live_51IvSZKJXrK78CsUSfSb5Jyjo3AkjZ2k6ZMr0c8miMMIcWcQiBKtCapD5ho2Bk45MjMh3QTlpLamkrOiG9gMJzMh100iGhW3ehO'
  )
  return stripe
}
