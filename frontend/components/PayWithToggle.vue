<template>
  <div class="w-full py-4">
    <div class="flex flex-row">
      <button
        type="button"
        :disabled="dappParameters.payWithOption==='ticket'"
        :class="{
          'bg-orange-600 text-white border-b-0': (dappParameters.payWithOption==='ticket'),
          'bg-gray-200 text-gray-800  hover:bg-gray-800 hover:bg-gray-100 hover:text-white': (
            dappParameters.payWithOption==='XRT')
        }"
        class="basis-1/2 uppercase py-2 px-4 text-gray-800 text-md"
        @click="dappParameters.payWithOption='ticket'"
      >
        Credit Card
      </button>
      <button
        type="button"
        :disabled="dappParameters.payWithOption==='XRT'"
        :class="{
          'bg-orange-600 text-white border-b-0': (dappParameters.payWithOption==='XRT'),
          'bg-gray-200 text-gray-800 hover:bg-gray-800 hover:bg-gray-100 hover:text-white': (
            dappParameters.payWithOption==='ticket')
        }"
        class="basis-1/2 uppercase py-2 px-4 text-gray-800 text-md"
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
