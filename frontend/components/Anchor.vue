<template>
  <a :id="props.anchorId" :href="props.hrefId">
    <h3
      :id="props.anchorId"
      class="w-full text-xl md:text-2xl font-bold mx-6 text-white"
    >
      {{ props.title }}
    </h3>
  </a>
</template>

<script>
import { defineComponent } from '@vue/composition-api'
export default defineComponent({
  props: ['anchorId', 'hrefId', 'title'],
  setup (props) {
    return { props }
  }
})
</script>
