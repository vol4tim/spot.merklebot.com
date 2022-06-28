<template>
  <div class="p-4 mt-4">
    <div class="container">
      <div class="flex flex-col md:grid grid-cols-12 text-gray-50">
        <slot />
      </div>
    </div>
  </div>
</template>
<script>
import { defineComponent } from '@nuxtjs/composition-api'
export default defineComponent({
  setup () {
  }
})
</script>
