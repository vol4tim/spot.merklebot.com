<template>
  <PayWithToggle>
    <template #ticket>
      <div class="w-full px-2 bg-gray-600 relative">
        <p class="text-md my-4 mb-16 text-white text-center">
          You have {{
            wallet.selectedAccount.tickets.filter(
              (ticket) => ticket.spent === false
            ).length
          }}
          tickets
        </p>
        <button
          type="button"
          class="
              absolute bottom-0 inset-x-0 uppercase py-2 mx-4 my-2 px-4 md:mt-16
              text-md text-center
              text-gray-800 bg-gray-200 border-2
              hover:bg-gray-100 hover:bg-gray-800 hover:text-white
            "
          :class="{'opacity-30 pointer-events-none': !canLaunchForTicket}"
          :disabled="!canLaunchForTicket"
          @click="sendCommandTicket"
        >
          Launch for 1 ticket
        </button>
      </div>
    </template>
    <template #XRT>
      <div class="w-full px-2 bg-gray-600 relative">
        <p class="text-md my-4 mb-16 text-white text-center">
          You have {{ wallet.selectedAccount.balanceFormatted }}
        </p>

        <button
          type="button"
          class="
              absolute bottom-0 inset-x-0 uppercase py-2 mx-4 my-2 px-4 md:mt-16
              text-md text-center
              text-gray-800 bg-gray-200 border-2
              hover:bg-gray-100 hover:bg-gray-800 hover:text-white
            "
          :class="{'opacity-30 pointer-events-none': !canLaunchForXrt}"
          :disabled="!canLaunchForXrt"
          @click="sendCommandXrt"
        >
          Launch for 1 XRT
        </button>
      </div>
    </template>
  </PayWithToggle>
</template>

<script>
import { defineComponent } from '@vue/composition-api'
import { computed } from '@nuxtjs/composition-api'
import { useDAppParameters } from '~/store'
import { useRobot } from '~/store/robot'
import { useWallet } from '~/store/wallet'

export default defineComponent({
  setup () {
    const dAppParameters = useDAppParameters()
    const robot = useRobot()
    const wallet = useWallet()

    const sendCommand = async (transferXrtAmount) => {
      console.log('Sending command')
      console.log(dAppParameters.currentDrawingSegments)
      const commandParams = {
        account: wallet.selectedAccount.account.address,
        payment_mode: transferXrtAmount ? 'xrt' : 'ticket',
        task_type: dAppParameters.currentDrawingSegments.length > 0 ? 'drawing' : 'inspection'
      }
      if (commandParams.task_type === 'drawing') {
        commandParams.segments = dAppParameters.currentDrawingSegments
      }
      try {
        const res = await robot.launchCps(transferXrtAmount, commandParams)
        if (res) {
          if (dAppParameters.currentDrawingSegments.length > 0) {
            robot.sendDrawing(commandParams.account, commandParams.segments, commandParams.paymentMode, `${res.txInfo.blockNumber}-${res.txInfo.txIndex}`)
          } else {
            // start time based inspection
            robot.startInspection(commandParams.account, commandParams.paymentMode, `${res.txInfo.blockNumber}-${res.txInfo.txIndex}`)
          }
        }
      } catch (e) {
        console.error(e)
      }
    }

    const sendCommandXrt = async () => {
      await sendCommand(1 * 10 ** 9) // 1 Wn, 1 Wn = 1 * 10 ^ -9 XRT
    }

    const sendCommandTicket = async () => {
      await sendCommand()
    }

    const canLaunchForXrt = computed(() => {
      const hasEnoughXrt = wallet.selectedAccount.balanceRaw * 10 ** -9 > 1
      return hasEnoughXrt && robot.robotState
    })

    const canLaunchForTicket = computed(() => {
      const hasTicket = wallet.selectedAccount.tickets.filter(ticket => ticket.spent === false).length >= 1
      return hasTicket && robot.robotState
    })

    return { sendCommandXrt, sendCommandTicket, wallet, canLaunchForXrt, canLaunchForTicket }
  }
})

</script>

<style scoped>

</style>
