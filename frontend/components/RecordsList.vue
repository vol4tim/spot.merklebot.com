<template>
  <div class="container flex flex-col mx-auto w-full items-center justify-center">
    <div class="px-4 py-5 sm:px-6 w-full border dark:bg-gray-800 bg-white shadow mb-2 rounded-md">
      <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white">
        Recorded sessions
      </h3>
      <div class="mt-1 max-w-2xl">
        <Toggle label="Show only my sessions" @toggled="(args)=>{filters.showOnlyMySessions = args.checked}" />
      </div>
    </div>
    <ul class="flex flex-col">
      <li v-for="(session, index) in sessions" :key="index" class="border-gray-400 flex flex-row mb-2">
        <NuxtLink :to="`/records/${session.id}`">
          <div class="transition duration-500 shadow ease-in-out transform hover:-translate-y-1 hover:shadow-lg select-none cursor-pointer bg-white dark:bg-gray-800 rounded-md flex flex-1 items-center p-4">
            <div class="flex flex-col w-100 h-100 justify-center items-center mr-4">
              <img alt="result" :src="`${session.traceFolderLink}/result.jpg`" class="mx-auto object-cover  h-100 w-100 ">
            </div>
            <div class="flex-1 pl-1 md:mr-16">
              <div class="font-medium dark:text-white">
                Session {{ session.id }}
              </div>
              <div class="text-gray-600 dark:text-gray-200 text-sm">
                From {{ session.sender }}
              </div>
            </div>
            <div class="text-gray-600 dark:text-gray-200 text-xs">
              {{ session.created_at }}
            </div>
            <button class="w-24 text-right flex justify-end">
              <svg
                width="12"
                fill="currentColor"
                height="12"
                class="hover:text-gray-800 dark:hover:text-white dark:text-gray-200 text-gray-500"
                viewBox="0 0 1792 1792"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M1363 877l-742 742q-19 19-45 19t-45-19l-166-166q-19-19-19-45t19-45l531-531-531-531q-19-19-19-45t19-45l166-166q19-19 45-19t45 19l742 742q19 19 19 45t-19 45z" />
              </svg>
            </button>
          </div>
        </NuxtLink>
      </li>
    </ul>
  </div>
</template>

<script>
import { defineComponent, useFetch, ref, reactive, computed } from '@nuxtjs/composition-api'
import { useWallet } from '../store/wallet'

export default defineComponent({
  setup () {
    const wallet = useWallet()

    const sessionsList = ref([])
    const filters = reactive({
      showOnlyMySessions: false
    })

    const sessions = computed(() => {
      return sessionsList.value.filter((session) => {
        let showSession = true
        if (filters.showOnlyMySessions && session.sender !== wallet.selectedAccount.account.address) {
          showSession = false
        }
        return showSession
      })
    })
    console.log(sessions.value)
    useFetch(async () => {
      const dbSessions = await (await fetch('https://api.merklebot.com/robonomics-launch-traces', { method: 'GET' })).json()

      dbSessions.forEach((session) => {
        session.traceFolderLink = `https://merklebot.mypinata.cloud/ipfs/${session.ipfs_cid}/spot/spot.merklebot.com/spot/traces/user-${session.sender}-cps-4FNQo2tK6PLeEhNEUuPePs8B8xKNwx15fX7tC2XnYpkC8W1j-session-${session.nonce}-${session.created_at}`
        sessionsList.value.push(session)
      })
      console.log(sessions.value)
    })
    return { sessions, wallet, filters }
  }

})

</script>
