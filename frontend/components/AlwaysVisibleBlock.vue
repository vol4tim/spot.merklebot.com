<template>
  <div class="px-6 py-4 sticky top-0">
    <div v-if="robot.robotState">
      <p class="text-3xl my-6 text-center text-white">
        Hi, I’m Spot 🦾🐶
      </p>
      <div>
        <CameraFrame interaction-mode="drawing" />
      </div>
      <p class="text-2xl my-6 text-center text-white">
        And we are a team of builders who share the vision of
        <br>
        <span class="text-orange-600 font-bold">machine economy with no single point of failure.</span>
      </p>

      <p class="text-2xl mt-2 text-center text-white">
        With this demo we aim to demonstrate the benefits of using Web3 software
        stack in robotics deployments.
        <br>
      </p>
    </div>
    <div v-if="!robot.robotState">
      <p class="text-3xl my-6 text-center text-red-600">
        Spot is currently unavailable
      </p>
      <div class="h-1/3">
        <CameraFrame interaction-mode="drawing" />
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from '@vue/composition-api'
import { useRobot } from '../store/robot'

export default defineComponent({
  setup () {
    const robot = useRobot()

    return { robot }
  }
})
</script>
