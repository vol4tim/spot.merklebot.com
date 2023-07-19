<template>
  <div>
    <p class="text-md mt-2 text-white">
      <span class="text-yellow-500">{{ info.name }}</span>
    </p>

    <img :src="info.image" class="mt-2" style="width:200px">

    <p class="text-md mt-2 text-white" style="overflow: scroll;max-width: 550px;">
      {{ info.description }}
    </p>
  </div>
</template>

<script>
export default {
  props: {
    info: {
      type: Object,
      default: null
    }
  }
}
</script>
