import axios from 'axios'

const client = axios.create({
  baseURL: 'https://api.merklebot.com/strelka'
})

export const calibrateSpot = async (accountAddress, signedToken) => {
  const resp = await client.post('start_calibration', {
    account: accountAddress,
    signed_token: signedToken
  })
  return resp
}
