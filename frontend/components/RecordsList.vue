<template>
  <div class="container flex flex-col mx-auto w-full items-center justify-center">
    <ul class="flex flex-col">
      <li v-for="(session, index) in sessions" :key="index" class="border-gray-400 flex flex-row mb-2">
        <NuxtLink :to="`/records/${session.session_id}`">
          <div class="transition duration-500 shadow ease-in-out transform hover:-translate-y-1 hover:shadow-lg select-none cursor-pointer bg-white dark:bg-gray-800 rounded-md flex flex-1 items-center p-4">
            <div class="flex flex-col w-100 h-100 justify-center items-center mr-4">
              <img alt="result" :src="`${session.traceFolderLink}/result.jpg`" class="mx-auto object-cover  h-100 w-100 ">
            </div>
            <div class="flex-1 pl-1 md:mr-16">
              <div class="font-medium dark:text-white">
                Session {{ session.session_id }}
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
export default {
  name: 'RecordsList',
  data: () => (
    {
      sessions: []
    }
  ),
  mounted () {
    this.fetchData()
  },
  methods: {
    async fetchData () {
      for (let i = 68; i <= 70; i++) {
        const sessionData = await (await fetch(`https://api.merklebot.com/davos/traces/session/${i}`, { method: 'GET' })).json()
        const session = { ...sessionData }
        session.traceFolderLink = `https://merklebot.mypinata.cloud/ipfs/${session.ipfs_cid}/spot/davos.merklebot.com/spot/traces/user-${session.user_account_address}-cps-4FNQo2tK6PLeEhNEUuPePs8B8xKNwx15fX7tC2XnYpkC8W1j-session-${session.session_id}-${session.created_at}`
        this.sessions.push(session)
      }
    }
  }
}
</script>
