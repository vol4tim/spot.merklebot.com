<template>
  <CardContainer title="Robot info">
    <p class="text-md mt-2 text-white">
      Robot state: <span class="text-yellow-500">{{ robot.robotState }}</span>
    </p>
    <p class="text-md mt-2 text-white">
      Tasks in queue: <span class="text-yellow-500">{{ robot.cps.queue }}</span>
    </p>
  </CardContainer>
</template>

<script>
import { defineComponent } from '@nuxtjs/composition-api'
import { useRobot } from '~/store/robot'
export default defineComponent({
  setup () {
    const robot = useRobot()
    return { robot }
  }
})
</script>
