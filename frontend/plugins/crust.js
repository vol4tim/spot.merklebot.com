import { ApiPromise, WsProvider } from '@polkadot/api'
import { typesBundleForPolkadot } from '@crustio/type-definitions'

const crustApi = new ApiPromise({
  provider: new WsProvider('wss://rpc.crust.network'),
  typesBundle: typesBundleForPolkadot
})

export const getCrustFileInfo = async (fileCid) => {
  await crustApi.isReady

  const fileInfo = await crustApi.query.market.filesV2(fileCid)
  return fileInfo.toHuman()
}
