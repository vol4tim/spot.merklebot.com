<template>
  <div>
    <div class="relative inline-block w-10 mr-2 align-middle select-none" @click="toggled">
      <input
        type="checkbox"
        name="toggle"
        :class="{'bg-blue-500 right-0': active, 'right-4': !active}"
        class=" outline-none focus:outline-none  duration-200 ease-in absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
      >
      <label class="block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer" />
    </div>
    <span class=" text-sm text-gray-500 dark:text-gray-200">
      {{ label }}
    </span>
  </div>
</template>

<script>
export default {
  name: 'Toggle',
  props: ['checked', 'label'],
  data: () => {
    return {
      active: false
    }
  },
  methods: {
    toggled () {
      console.log('toggled')
      this.active = !this.active
      this.$emit('toggled', { checked: this.active })
    }
  }
}
</script>

<style scoped>

</style>
