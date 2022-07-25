<template>
  <main class="bg-gray-800 font-mono text-white m-8">
    <UserInfoSurvey />
  </main>
</template>

<script>
import { defineComponent } from '@nuxtjs/composition-api'
import UserInfoSurvey from '../components/UserInfoSurvey.vue'

export default defineComponent({
  components: { UserInfoSurvey },
  setup () {}
})
</script>
