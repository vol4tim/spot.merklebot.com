<template>
  <div class="flex md:contents">
    <div class="col-start-0 col-end-2 mr-10 md:mx-auto relative">
      <div class="h-full w-6 flex items-center justify-center">
        <div class="h-full w-1 pointer-events-none" :class="{'bg-green-500': (status==='success'),'bg-orange-600': (status==='wait'), 'bg-gray-300': (status==='disabled')}" />
      </div>
      <div class="w-6 h-6 absolute top-1/2 -mt-3 rounded-full  shadow text-center" :class="{'bg-green-500': (status==='success'),'bg-orange-600': (status==='wait'), 'bg-gray-300': (status==='disabled')}">
        <i class="fas fa-check-circle text-white" />
      </div>
    </div>
    <div class="col-start-2 col-end-12 p-4 my-4 mr-auto border-2 bg-gray-700  w-full" :class="{'border-green-500': (status==='success'), 'border-gray-600': (status!=='success'), 'opacity-30 pointer-events-none': (status==='disabled')}">
      <h3
        id="anchor-to-1"
        class="max-w-md text-xl md:text-2xl font-bold mx-6 text-white"
      >
        {{ elementTitle }}
      </h3>
      <slot />
    </div>
  </div>
</template>

<script>
import { defineComponent } from '@nuxtjs/composition-api'
export default defineComponent({
  props: ['title', 'status'],
  setup (props) {
    const elementTitle = props.title
    const elementStatus = props.status
    return { elementTitle, elementStatus }
  }
})
</script>
