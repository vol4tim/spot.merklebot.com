<template>
  <div class="bg-gray-700">
    <figure v-if="spot.cameraImages[camera]">
      <img :src="'data:image/jpeg;base64, '+ spot.cameraImages[camera]" alt="Video stream">
    </figure>
    <div v-else class="mx-16 my-8">
      Waiting for image
    </div>
    <div class="p-2">
      <p class="font-mono text-white">
        {{ cameraTitle }}
      </p>
    </div>
  </div>
</template>

<script>
import { defineComponent } from '@nuxtjs/composition-api'
import { useSpot } from '~/store/spot'

export default defineComponent({

  props: ['title', 'cameraName'],
  setup (props) {
    const spot = useSpot()
    const cameraTitle = props.title
    const camera = props.cameraName

    return { cameraTitle, camera, spot }
  }
})
</script>
