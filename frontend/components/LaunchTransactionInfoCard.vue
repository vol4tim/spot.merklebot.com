<template>
  <CardContainer title="Launch info">
    <p class="text-md mt-2 text-white">
      approve status: <span class="text-yellow-500">{{ robot.cps.approve.status }}</span>
    </p>

    <p v-if="robot.cps.approve.tx" class="text-md mt-2 text-white">
      approve tx:
      <a
        class="text-yellow-500"
        :href="`https://neonscan.org/tx/${robot.cps.approve.txs}`"
        target="_blank"
        rel="noopener noreferrer"
      >{{ addressShort(robot.cps.approve.tx) }}</a>
    </p>

    <p class="text-md mt-2 text-white">
      liability address:
      <a
        class="text-yellow-500"
        :href="`https://neonscan.org/address/${robot.cps.liability.address}`"
        target="_blank"
        rel="noopener noreferrer"
      >{{ addressShort(robot.cps.liability.address) }}</a>
    </p>

    <p class="text-md mt-2 text-white">
      liability result: <span class="text-yellow-500">{{ robot.cps.liability.result }}</span>
    </p>

    <!-- <p class="text-md mt-2 text-white">
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
    </p> -->
  </CardContainer>
</template>

<script>
import { defineComponent } from '@vue/composition-api'
import { addressShort, makeSubscanLink } from '~/plugins/robonomics'
import { useRobot } from '~/store/robot'

export default defineComponent({
  setup () {
    const robot = useRobot()

    return { robot, makeSubscanLink, addressShort }
  }
})
</script>
