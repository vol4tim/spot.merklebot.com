<template>
  <CardContainer title="Launch info">
    <p class="text-md mt-2 text-white">
      launch status: <span class="text-yellow-500">{{ robot.cps.status }}</span>
    </p>

    <p class="text-md mt-2 text-white">
      Tx status: <span class="text-yellow-500">{{ robot.cps.launch.txStatus }}</span>
    </p>

    <p class="text-md mt-2 text-white">
      Transaction: <a
        class="text-yellow-500"
        :href="
          makeSubscanLink('robonomics', robot.cps.launch.txInfo.tx)
        "
        target="_blank"
        rel="noopener noreferrer"
      >{{ addressShort(robot.cps.launch.txInfo.tx) }}</a>
    </p>
  </CardContainer>
</template>

<script>
import { defineComponent } from '@vue/composition-api'
import { useRobot } from '~/store/robot'
import { makeSubscanLink, addressShort } from '~/plugins/robonomics'

export default defineComponent({
  setup () {
    const robot = useRobot()

    return { robot, makeSubscanLink, addressShort }
  }
})
</script>
