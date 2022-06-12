<template>
  <div class="m-4 min-h-200 p-2">
    <div>
      <p class="text-md mt-2 dark:text-white mx-6">
        Robot state: <span class="text-yellow-500">{{ robot.robotState }}</span>
      </p>

      <p class="text-md mt-2 dark:text-white mx-6">
        Robot status: <span class="text-yellow-500">{{ robot.cps.status }}</span>
      </p>

      <p class="text-md mt-2 dark:text-white mx-6">
        Transaction status: <span class="text-yellow-500">{{ robot.cps.launch.txStatus }}</span>
      </p>

      <p class="text-md mt-2 dark:text-white mx-6">
        View transaction: <a
          class="text-yellow-500"
          :href="
            'https://robonomics.subscan.io/extrinsic/' + robot.cps.launch.txInfo.tx
          "
          target="_blank"
          rel="noopener noreferrer"
        >{{ addressShort(robot.cps.launch.txInfo.tx) }}</a>
      </p>
    </div>

    <div v-if="launchData!==null">
      <p class="text-md mt-2 dark:text-white mx-6">
        IPFS Content ID: <span class="text-yellow-500">{{ launchData.ipfs_cid }}</span>
      </p>
      <p class="text-md mt-2 dark:text-white mx-6">
        View Robonomics Launch Tx: <a :href="datalogLink" class="text-yellow-500" target="_blank" rel="noopener noreferrer">{{ launchLink }}</a>
      </p>
      <p class="text-md mt-2 dark:text-white mx-6">
        View record data on IPFS: <a :href="traceFolderLink" class="text-yellow-500" target="_blank" rel="noopener noreferrer">{{ traceFolderLink.slice(0, 50) + '...' }}</a>
      </p>
      <p class="text-md mt-2 dark:text-white mx-6">
        View Robonomics Datalog Tx:<a :href="datalogLink" class="text-yellow-500" target="_blank" rel="noopener noreferrer">{{ datalogLink.slice(0, 50) + '...' }}</a>
      </p>

      <div class="flex items-left justify-left m-4">
        <video :src="`${traceFolderLink}/h264_camera.mp4`" type="video/mp4" controls />
      </div>
    </div>

    <div v-else>
      <p class="text-md mt-2 dark:text-white mx-6">
        Your launch data will appear here after processing drawing and saving all data
      </p>
    </div>
  </div>
</template>
<script>
import { defineComponent, onMounted, ref } from '@nuxtjs/composition-api'
import { useRobot } from '../store/robot'
import { readRobonomicsLaunchTracesBySender } from '../plugins/merklebot'
export default defineComponent({
  setup () {
    const robot = useRobot()

    const launchData = ref(null)
    const traceFolderLink = ref(null)
    const launchLink = ref(null)
    const datalogLink = ref(null)

    const addressShort = (address) => {
      if (!address) {
        return ''
      }
      return address.slice(0, 6) + '...' + address.slice(-4)
    }

    const updateLaunchData = async () => {
      if (robot.cps.launch.txStatus) {
        try {
          const res = await readRobonomicsLaunchTracesBySender({ launchTxId: `${robot.cps.launch.txInfo.blockNumber}-${robot.cps.launch.txInfo.txIndex}` })
          console.log(res)
          if (res) {
            launchData.value = res
            traceFolderLink.value = `https://merklebot.mypinata.cloud/ipfs/${res.ipfs_cid}/spot/davos.merklebot.com/spot/traces/user-${res.sender}-cps-4FNQo2tK6PLeEhNEUuPePs8B8xKNwx15fX7tC2XnYpkC8W1j-session-${res.nonce}-${res.created_at}`
            launchLink.value = `https://robonomics.subscan.io/extrinsic/${res.launch_tx_id}`
            datalogLink.value = `https://robonomics.subscan.io/extrinsic/${res.datalog_tx_id}`
          }
        } catch (e) {

        }
      }
      setTimeout(updateLaunchData, 1000)
    }

    onMounted(() => {
      updateLaunchData()
    })
    return {
      robot, launchData, traceFolderLink, launchLink, datalogLink, addressShort
    }
  }
})
</script>
