import axios from 'axios'

// const client = axios.create({
//   baseURL: 'https://api.merklebot.com/strelka'
// })
const client = axios.create({
  baseURL: 'https://api.merklebot.com/strelka'
  // baseURL: 'http://172.24.5.211:1234'
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
    value: vel
  })
  return resp
}

export const poseSpot = async (accountAddress, signedToken, poseName) => {
  const resp = await client.post('command', {
    account: accountAddress,
    signed_token: signedToken,
    action: 'pose',
    value: poseName
  })
  return resp
}
