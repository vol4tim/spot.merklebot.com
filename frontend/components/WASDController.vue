<template>
  <div class="grid grid-cols-3 gap-x-4">
    <div />
    <button
      type="button"
      class="uppercase text-md w-full py-2 my-2 px-1 bg-gray-200 text-gray-800
        hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
      @click="()=>moveCommand({x:1, y:0})"
    >
      Up
    </button>
    <div />
    <button
      type="button"
      class="uppercase text-md w-full py-2 my-2 px-1 bg-gray-200 text-gray-800
        hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
      @click="()=>moveCommand({x:0, y:-1})"
    >
      Left
    </button>
    <button
      type="button"
      class="uppercase text-md w-full py-2 my-2 px-1 bg-gray-200 text-gray-800
        hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
      @click="()=>moveCommand({x:-1, y:0})"
    >
      Down
    </button>
    <button
      type="button"
      class="uppercase text-md w-full py-2 my-2 px-1 bg-gray-200 text-gray-800
        hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
      @click="()=>moveCommand({x:0, y:1})"
    >
      Right
    </button>
  </div>
</template>
<script>
import { defineComponent, onMounted } from '@vue/composition-api'
import { moveSpot } from '~/plugins/robot'
import { useRobot } from '~/store/robot'
import { useWallet } from '~/store/wallet'

export default defineComponent({
  setup () {
    const wallet = useWallet()
    const robot = useRobot()

    const moveCommand = async (vel) => {
      await moveSpot(wallet.selectedAccount.account.address, robot.signedRobotToken, vel)
    }
    onMounted(() => {
      document.addEventListener('keydown', (event) => {
        const name = event.key
        if (name === 'w') {
          moveCommand({ x: 0.45, y: 0, r: 0 })
        } else if (name === 'a') {
          moveCommand({ x: 0, y: 0.4, r: 0 })
        } else if (name === 's') {
          moveCommand({ x: -0.4, y: 0, r: 0 })
        } else if (name === 'd') {
          moveCommand({ x: 0, y: -0.4, r: 0 })
        } else if (name === 'q') {
          moveCommand({ x: 0, y: 0, r: 0.4 })
        } else if (name === 'e') {
          moveCommand({ x: 0, y: 0, r: -0.4 })
        }
      }, false)
    })
    return { moveCommand }
  }
})
</script>
