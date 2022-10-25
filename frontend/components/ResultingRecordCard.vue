<template>
  <div class="m-4 min-h-200 p-2">
    <div />

    <div class="mt-4">
      <CardContainer title="Saved data">
        <div v-if="launchData!==null">
          <p class="text-md mt-2 text-white">
            Robonomics Launch Tx: <a
              :href="makeSubscanLink('robonomics', launchTxId)"
              class="text-yellow-500"
              target="_blank"
              rel="noopener noreferrer"
            >{{ addressShort(launchTxId) }}</a>
          </p>
          <p class="text-md mt-2 text-white">
            Record data on IPFS: <a
              v-if="traceInfo.ipfsCid"
              :href="makeIpfsFolderLink(traceInfo)"
              class="text-yellow-500"
              target="_blank"
              rel="noopener noreferrer"
            >{{ addressShort(traceInfo.ipfsCid) }}</a>
            <Spinner v-else />
          </p>
          <p class="text-md mt-2 text-white">
            Robonomics Datalog Tx: <a
              v-if="datalogTxId"
              :href="makeSubscanLink('robonomics', datalogTxId)"
              class="text-yellow-500"
              target="_blank"
              rel="noopener noreferrer"
            >{{ addressShort(datalogTxId) }}</a>
            <Spinner v-else />
          </p>
          <p class="text-md mt-2 text-white">
            Crust Storage Order Tx: <a
              v-if="crustTxId"
              :href="makeSubscanLink('crust', crustTxId)"
              class="text-yellow-500"
              target="_blank"
              rel="noopener noreferrer"
            >{{ addressShort(crustTxId) }}</a>
            <Spinner v-else />
          </p>

          <div class="flex items-left justify-left m-4">
            <video :src="`${makeIpfsFolderLink(traceInfo)}/h264_camera.mp4`" type="video/mp4" controls />
          </div>
        </div>

        <div v-else>
          <p class="text-md mt-2 text-white">
            Your launch data will appear here after processing drawing and saving all data
          </p>
        </div>
      </CardContainer>
      <CardContainer>
        <NftInfo />
      </CardContainer>
    </div>
  </div>
</template>
<script>
import { defineComponent, onMounted, ref } from '@nuxtjs/composition-api'
import { useRobot } from '../store/robot'
import { readRobonomicsLaunchTracesBySender, makeIpfsFolderLink } from '../plugins/merklebot'
import { makeSubscanLink } from '~/plugins/robonomics'
import Spinner from '~/components/Spinner'
import NftInfo from '~/components/NftInfo.vue'

export default defineComponent({
  components: {
    Spinner,
    NftInfo
  },
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
            robot.cps.launch.recordData = res
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

    return {
      robot,
      launchData,
      traceInfo,
      launchTxId,
      datalogTxId,
      crustTxId,
      addressShort,
      makeSubscanLink,
      makeIpfsFolderLink
    }
  }
})
</script>
