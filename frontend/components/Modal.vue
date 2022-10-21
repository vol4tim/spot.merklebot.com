<template>
  <div>
    <div v-if="show" class="fixed z-10 overflow-y-auto top-0 w-full left-0 ">
      <div class="flex items-center justify-center min-height-100vh pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 transition-opacity">
          <div class="absolute inset-0 bg-gray-900 opacity-75" />
        </div>

        <div class="inline-block align-center bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full" role="dialog" aria-modal="true" aria-labelledby="modal-headline">
          <div class="shadow-lg px-4 py-2 w-full bg-gray-600 relative">
            <p class="text-lg w-max text-white font-semibold border-b border-gray-200">
              Success
            </p>

            <p class="text-white mt-4">
              Ticket successfully got. XRT for launch will be sent to your account during the next one minute in one of the next few blocks.
            </p>
            <div class="px-4 py-3 text-right">
              <button
                type="button"
                class="uppercase text-md w-full py-2 my-2 px-4 bg-gray-200 text-gray-800
        hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
                @click="closeModal"
              >
                Got it!
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref } from '@nuxtjs/composition-api'

export default defineComponent({
  emits: ['showModal'],
  setup ({ emit }) {
    const show = ref(false)

    const closeModal = () => {
      show.value = false
    }
    const openModal = () => {
      show.value = true
    }

    return { show, closeModal, openModal }
  }
})
</script>
