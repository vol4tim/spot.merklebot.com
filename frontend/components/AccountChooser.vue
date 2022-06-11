<template>
  <div>
    <div class="relative p-1 flex items-center w-full space-x-4 justify-end">
      <div class="w-128">
        <div v-if="wallet.selectedAccount.account" class="mt-1 relative">
          <button
            type="button"
            class="relative w-full bg-white dark:bg-gray-600 dark:text-white rounded-md shadow-lg pl-3 pr-10 py-3 text-left cursor-default focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:focus:ring-white sm:text-sm"
            @click="()=>showAccountChoose = !showAccountChoose"
          >
            <span class="flex items-center">

              <img
                :src="`https://avatars.dicebear.com/api/identicon/${wallet.selectedAccount.account.address}.svg`"
                alt="person"
                class="flex-shrink-0 h-6 w-6 rounded-full"
              >
              <span class="ml-3 block truncate">
                {{ wallet.selectedAccount.account.meta.name }} - ({{
                  wallet.selectedAccount.balanceFormatted
                }}) - {{ addressShort(wallet.selectedAccount.account.address) }}
              </span>
            </span>
            <span class="ml-3 absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
              <svg
                class="h-5 w-5 text-gray-400"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                  clip-rule="evenodd"
                />
              </svg>
            </span>
          </button>
          <div v-show="showAccountChoose" class="absolute mt-1 w-full z-10 rounded-md bg-white dark:bg-gray-600 shadow-lg">
            <ul
              tabindex="-1"
              role="listbox"
              aria-labelledby="listbox-label"
              aria-activedescendant="listbox-item-3"
              class="max-h-56 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm"
            >
              <li
                v-for="(account, idx) in wallet.accounts"
                id="listbox-item-0"
                :key="idx"
                :value="account"
                role="option"
                class="text-gray-900 dark:text-white  cursor-default hover:bg-indigo-500 hover:text-white select-none relative py-2 pl-3 pr-9"
                @click="()=>{selectAccount(account); showAccountChoose=false}"
              >
                <div class="flex items-center">
                  <img
                    :src="`https://avatars.dicebear.com/api/identicon/${account.address}.svg`"
                    alt="person"
                    class="flex-shrink-0 h-6 w-6 rounded-full"
                  >
                  <span class="ml-3 block font-normal truncate">
                    {{ account.meta.name }} - {{ addressShort(account.address) }}
                  </span>
                </div>
                <span
                  v-show="wallet.selectedAccount.account.address===account.address"
                  class="absolute inset-y-0 right-0 flex items-center pr-4"
                >
                  <svg
                    class="h-5 w-5"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, onMounted, ref } from '@nuxtjs/composition-api'

import { useWallet } from '@/store/wallet'
export default defineComponent({
  setup () {
    const wallet = useWallet()
    const showAccountChoose = ref(false)

    onMounted(() => {
      wallet.connectWallet()
    })

    const addressShort = (address) => {
      return address.slice(0, 6) + '...' + address.slice(-4)
    }

    const selectAccount = (account) => {
      wallet.setActiveAccount(account)
    }
    return {
      showAccountChoose,
      selectAccount,
      addressShort,
      wallet
    }
  }
})

</script>
