<template>
  <div class="grid grid-cols-2 gap-x-4">
    <button
      type="button"
      class="uppercase text-md w-full py-2 my-2 px-1 bg-gray-200 text-gray-800
        hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
      @click="()=>poseCommand('stance')"
    >
      Stance sides
    </button>
    <button
      type="button"
      class="uppercase text-md w-full py-2 my-2 px-1 bg-gray-200 text-gray-800
        hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
      @click="()=>poseCommand('stance_0')"
    >
      Stance default
    </button>
    <button
      type="button"
      class="uppercase text-md w-full py-2 my-2 px-1 bg-gray-200 text-gray-800
        hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
      @click="()=>poseCommand('seat')"
    >
      Seat
    </button>
    <button
      type="button"
      class="uppercase text-md w-full py-2 my-2 px-1 bg-gray-200 text-gray-800
        hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
      @click="()=>poseCommand('stand')"
    >
      Stand
    </button>
    <button
      type="button"
      class="uppercase text-md w-full py-2 my-2 px-1 bg-gray-200 text-gray-800
        hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
      @click="()=>poseCommand('bow')"
    >
      Bow
    </button>
    <button
      type="button"
      class="uppercase text-md w-full py-2 my-2 px-1 bg-gray-200 text-gray-800
        hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
      @click="()=>poseCommand('bow_b')"
    >
      Bow boston
    </button>
    <button
      type="button"
      class="uppercase text-md w-full py-2 my-2 px-1 bg-gray-200 text-gray-800
        hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
      @click="()=>poseCommand('dust_off')"
    >
      Dust off
    </button>
  </div>
</template>
<script>
import { defineComponent } from '@vue/composition-api'
import { poseSpot } from '~/plugins/robot'
import { useRobot } from '~/store/robot'
import { useWallet } from '~/store/wallet'

export default defineComponent({
  setup () {
    const wallet = useWallet()
    const robot = useRobot()

    const poseCommand = async (poseName) => {
      await poseSpot(wallet.selectedAccount.account.address, robot.signedRobotToken, poseName)
    }

    return { poseCommand }
  }
})
</script>
