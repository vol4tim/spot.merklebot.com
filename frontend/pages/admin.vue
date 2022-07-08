<template>
  <main class="bg-gray-800 font-mono overflow-hidden">
    <div class="z-20 container mx-auto flex flex-row flex-wrap justify-center place-items-center">
      <div class="basis-5/12">
        <AlwaysVisibleBlock />
      </div>

      <div class="basis-7/12 flex">
        <AdminControlsBlock />
      </div>
    </div>
  </main>
</template>

<script>
import { defineComponent, onMounted } from '@nuxtjs/composition-api'
import { useRobot } from '../store/robot'

export default defineComponent({
  setup () {
    const robot = useRobot()

    const doRobotStatePolling = async () => {
      try {
        await robot.updateRobotState()
      } catch (e) {
        console.log('Spot state unavailable, retrying')
      }
      setTimeout(doRobotStatePolling, 1000)
    }

    onMounted(() => {
      doRobotStatePolling()
    })

    return {
    }
  }
})

</script>

<style scoped>
.screen {
  min-height: 80vh;
}
</style>
