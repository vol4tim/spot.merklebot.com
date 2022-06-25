<template>
  <div class="m-4 min-h-200 p-2">
    <div />
    <div class="grid grid-cols-2 gap-4">
      <CardContainer title="Robot info">
        <p class="text-md mt-2 dark:text-white">
          Robot state: <span class="text-yellow-500">{{ robot.robotState }}</span>
        </p>
        <p class="text-md mt-2 dark:text-white">
          Drawings in queue: <span class="text-yellow-500">{{ robot.queueSize }}</span>
        </p>
      </CardContainer>
      <CardContainer title="Launch info">
        <p class="text-md mt-2 dark:text-white">
          launch status: <span class="text-yellow-500">{{ robot.cps.status }}</span>
        </p>

        <p class="text-md mt-2 dark:text-white">
          Tx status: <span class="text-yellow-500">{{ robot.cps.launch.txStatus }}</span>
        </p>

        <p class="text-md mt-2 dark:text-white">
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
    </div>
    <div class="mt-4">
      <CardContainer title="Saved data">
        <div v-if="launchData!==null">
          <p class="text-md mt-2 dark:text-white">
            Robonomics Launch Tx: <a :href="makeSubscanLink('robonomics', launchTxId)" class="text-yellow-500" target="_blank" rel="noopener noreferrer">{{ addressShort(launchTxId) }}</a>
          </p>
          <p class="text-md mt-2 dark:text-white">
            Record data on IPFS: <a :href="makeIpfsFolderLink('traceInfo')" class="text-yellow-500" target="_blank" rel="noopener noreferrer">{{ addressShort(traceInfo.ipfsCid) }}</a>
          </p>
          <p class="text-md mt-2 dark:text-white">
            Robonomics Datalog Tx: <a :href="makeSubscanLink('robonomics', datalogTxId)" class="text-yellow-500" target="_blank" rel="noopener noreferrer">{{ addressShort(datalogTxId) }}</a>
          </p>
          <p class="text-md mt-2 dark:text-white">
            Crust Storage Order Tx: <a :href="makeSubscanLink('crust', crustTxId)" class="text-yellow-500" target="_blank" rel="noopener noreferrer">{{ addressShort(crustTxId) }}</a>
          </p>

          <div class="flex items-left justify-left m-4">
            <video :src="`${makeIpfsFolderLink(traceInfo)}/h264_camera.mp4`" type="video/mp4" controls />
          </div>
        </div>

        <div v-else>
          <p class="text-md mt-2 dark:text-white">
            Your launch data will appear here after processing drawing and saving all data
          </p>
        </div>
      </CardContainer>
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
    const traceInfo = ref(null)
    const launchTxId = ref(null)
    const datalogTxId = ref(null)
    const crustTxId = ref(null)

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
            traceInfo.value = {
              ipfsCid: res.ipfs_cid,
              sender: res.sender,
              nonce: res.nonce,
              createdAt: res.created_at

            }
            launchTxId.value = res.launch_tx_id
            datalogTxId.value = res.datalog_tx_id
            crustTxId.value = res.crust_tx_id
          }
        } catch (e) {

        }
      }
      setTimeout(updateLaunchData, 1000)
    }

    onMounted(() => {
      updateLaunchData()
    })

    const makeSubscanLink = (network, suffix) => {
      return `https://${network}.subscan.io/extrinsic/${suffix}`
    }

    const makeIpfsFolderLink = ({ ipfsCid, sender, nonce, createdAt }) => {
      return `https://merklebot.mypinata.cloud/ipfs/${ipfsCid}/spot/spot.merklebot.com/spot/traces/user-${sender}-cps-4FNQo2tK6PLeEhNEUuPePs8B8xKNwx15fX7tC2XnYpkC8W1j-session-${nonce}-${createdAt}`
    }

    return {
      robot, launchData, traceInfo, launchTxId, datalogTxId, crustTxId, addressShort, makeSubscanLink, makeIpfsFolderLink
    }
  }
})
</script>
