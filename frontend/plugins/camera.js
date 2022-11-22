import axios from 'axios'

const client = axios.create({
  baseURL: 'https://api.merklebot.com/videoserver'
})

const spotClient = axios.create({
  baseURL: 'https://api.merklebot.com/strelka'
})

export const getAuthToken = async (accountAddress) => {
  const resp = await spotClient.post('token', {
    account: accountAddress
  })

  return resp.data.token
}
export const moveCamera = async (accountAddress, signedToken, vel) => {
  const resp = await client.post('control', {
    account: accountAddress,
    signed_token: signedToken,
    control_name: 'move',
    velocity: vel
  })
  return resp
}

export const zoom = async (accountAddress, signedToken, zoomAbsolute) => {
  const resp = await client.post('control', {
    account: accountAddress,
    signed_token: signedToken,
    control_name: 'zoom',
    zoom_absolute: zoomAbsolute
  })
  return resp
}
