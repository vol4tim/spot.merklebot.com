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

export const moveSpot = async (accountAddress, signedToken, vel) => {
  const resp = await client.post('command', {
    account: accountAddress,
    signed_token: signedToken,
    action: 'move',
    vel
  })
  return resp
}
