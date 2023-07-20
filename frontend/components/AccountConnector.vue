<template>
  <div class="px-3">
    <div>
      <div v-if="!active">
        <button
          v-for="(newConnector, name) in connectorsByName"
          :key="name"
          class="uppercase py-2 px-4 text-gray-800 text-md bg-gray-200 text-gray-800 hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
          @click="setActivatingConnector(newConnector)"
        >
          Connect <span v-if="activatingConnector === newConnector">...</span>
        </button>
      </div>

      <div>
        <button
          v-if="active"
          class="uppercase py-2 px-4 text-gray-800 text-md bg-gray-200 text-gray-800 hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
          @click="deactivate"
        >
          Deactivate
        </button>
      </div>
    </div>

    <div v-if="!!error">
      <p class="text-xl my-6 text-center text-white font-bold">
        {{ getErrorMessage(error) }}
      </p>
    </div>
  </div>
</template>

<script>
import { UnsupportedChainIdError, useWeb3 } from '@instadapp/vue-web3'
import { defineComponent, ref } from '@nuxtjs/composition-api'
import { UserRejectedRequestError as UserRejectedRequestErrorFrame } from '@web3-react/frame-connector'
import { NoEthereumProviderError, UserRejectedRequestError as UserRejectedRequestErrorInjected } from '@web3-react/injected-connector'
import { UserRejectedRequestError as UserRejectedRequestErrorWalletConnect } from '@web3-react/walletconnect-connector'
import { injected } from '~/connectors'
import { useEagerConnect } from '~/connectors/useEagerConnect'

const ConnectorNames = {
  Injected: 'Injected'
}

const connectorsByName = {
  [ConnectorNames.Injected]: injected
}

function getErrorMessage (error) {
  if (error instanceof NoEthereumProviderError) {
    return 'No Ethereum browser extension detected, install MetaMask on desktop or visit from a dApp browser on mobile.'
  } else if (error instanceof UnsupportedChainIdError) {
    return "You're connected to an unsupported network."
  } else if (
    error instanceof UserRejectedRequestErrorInjected ||
    error instanceof UserRejectedRequestErrorWalletConnect ||
    error instanceof UserRejectedRequestErrorFrame
  ) {
    return 'Please authorize this website to access your Ethereum account.'
  } else {
    console.error(error)
    return 'An unknown error occurred. Check the console for more details.'
  }
}

export default defineComponent({
  setup () {
    const { active, activate, deactivate, connector, error } = useWeb3()
    useEagerConnect()

    const activatingConnector = ref()

    const setActivatingConnector = async (newConnector) => {
      activatingConnector.value = newConnector
      await activate(newConnector)
      activatingConnector.value = undefined
    }

    return {
      active,
      activate,
      deactivate,
      connectorsByName,
      connector,
      getErrorMessage,
      error,
      setActivatingConnector,
      activatingConnector
    }
  }
})
</script>
