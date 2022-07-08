import axios from 'axios'

const client = axios.create({
  baseURL: 'https://api.merklebot.com/videoserver'
})

export const getAuthToken = async (accountAddress) => {
  const resp = await client.post('token', {
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
