// import { Web3Provider } from '@ethersproject/providers'
import { setWeb3LibraryCallback } from '@instadapp/vue-web3'
import { InjectedConnector } from '@web3-react/injected-connector'
import Web3 from 'web3'

function getLibrary (provider) {
  // const library = new Web3Provider(provider)
  const library = new Web3(provider)
  library.pollingInterval = 12000
  return library
}

setWeb3LibraryCallback(getLibrary)

export const injected = new InjectedConnector({
  supportedChainIds: [245022926]
})
