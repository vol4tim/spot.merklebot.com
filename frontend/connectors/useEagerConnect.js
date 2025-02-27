import { useWeb3 } from '@instadapp/vue-web3'
import { onMounted, ref, watch } from '@nuxtjs/composition-api'
import { injected } from './index'

export function useEagerConnect () {
  const { activate, active } = useWeb3()

  const tried = ref(false)

  onMounted(() => {
    injected.isAuthorized().then((isAuthorized) => {
      if (isAuthorized) {
        activate(injected, undefined, true).catch(() => {
          tried.value = true
        })
      } else {
        tried.value = true
      }
    })
  })

  // if the connection worked, wait until we get confirmation of that to flip the flag
  watch([tried, active], () => {
    if (!tried.value && active.value) {
      tried.value = true
    }
  })

  return {
    tried
  }
}
