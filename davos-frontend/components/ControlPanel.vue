<template>
  <div class="mb-3">
    <div class="relative inline-block w-10 mr-2 align-middle select-none">
      <input v-model="checked" type="checkbox" name="toggle" id="Blue"
             class=" outline-none focus:outline-none  duration-200 ease-in absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
             :class="{'bg-blue-500': checked, 'right-0': checked, 'right-4': !checked}"
      />
      <label for="Blue" class="block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer">
      </label>
    </div>
    <span class="text-gray-400 font-medium">
               Detect faces
            </span>
  </div>

</template>

<script>
export default {
  name: "ControlPanel",
  data () {
    return {
      checked: false
    }
  }
}
</script>

<style scoped>

</style>
