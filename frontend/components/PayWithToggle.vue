<template>
  <div class="w-full py-4">
    <div class="flex flex-row ">
      <button
        type="button"
        :class="{'dark:bg-gray-600 dark:text-white border-b-0': (dappParameters.payWithOption==='ticket'), 'dark:bg-white dark:text-gray-800  hover:bg-gray-800 hover:dark:bg-gray-100 hover:text-white': (dappParameters.payWithOption==='XRT')}"
        class="basis-1/2 uppercase py-2 px-4  bg-transparent border-0 border-gray-800 text-gray-800 dark:text-white text-md"
        @click="dappParameters.payWithOption='ticket'"
      >
        Credit Card
      </button>
      <button
        type="button"
        :class="{'dark:bg-gray-600 dark:text-white border-b-0': (dappParameters.payWithOption==='XRT'), 'dark:bg-white dark:text-gray-800  hover:bg-gray-800 hover:dark:bg-gray-100 hover:text-white': (dappParameters.payWithOption==='ticket')}"
        class="basis-1/2 uppercase py-2 px-4  bg-transparent border-0 border-gray-800 text-gray-800 dark:text-white text-md"
        @click="dappParameters.payWithOption='XRT'"
      >
        Crypto
      </button>
    </div>
    <div>
      <div class="flex flex-row ">
        <slot v-if="dappParameters.payWithOption==='XRT'" name="XRT" />
        <slot v-if="dappParameters.payWithOption==='ticket'" name="ticket" />
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from '@nuxtjs/composition-api'
import { useDAppParameters } from '../store'
export default defineComponent({
  setup () {
    const dappParameters = useDAppParameters()

    return {
      dappParameters
    }
  }
})
</script>
