<template>
  <div class="w-full">
    <div class="shadow-lg px-4 py-2 w-full bg-white dark:bg-gray-600 relative">
      <p class="text-lh w-max text-gray-700 dark:text-white font-semibold border-b border-gray-200">
        {{ title }}
      </p>
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  name: 'CardContainer',
  props: {
    title: {
      type: String,
      required: false
    }
  }
}
</script>

<style scoped>

</style>
