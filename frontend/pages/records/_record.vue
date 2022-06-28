<template>
  <main class="bg-gray-800 h-screen overflow-hidden relative">
    <div class="flex items-start justify-between">
      <SidePanel active="Records" />
      <div class="flex flex-col w-full md:space-y-4">
        <HeaderPanel />
        <div class="overflow-auto h-screen pb-24 px-4 md:px-6">
          <div v-if="!txId">
            <h1 class="text-4xl font-semibold text-white">
              Sessions
            </h1>
            <div class="grid grid-cols-1 gap-4 my-4">
              <RecordsList />
            </div>
          </div>
          <div v-if="txId">
            <h1 class="text-4xl font-semibold text-white">
              Session {{ txId }}
            </h1>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4 my-4">
              <CardContainer v-if="launchData" title="Launch data">
                <p class="text-md mt-2 text-white">
                  Robonomics Launch Tx: <a
                    :href="makeSubscanLink(launchTxId)"
                    class="text-yellow-500"
                    target="_blank"
                    rel="noopener noreferrer"
                  >{{ addressShort(launchTxId) }}</a>
                </p>
                <p class="text-md mt-2 text-white">
                  Record data on IPFS: <a
                    :href="makeIpfsFolderLink(traceInfo)"
                    class="text-yellow-500"
                    target="_blank"
                    rel="noopener noreferrer"
                  >{{ addressShort(launchData.ipfs_cid) }}</a>
                </p>
                <p class="text-md mt-2 text-white">
                  Robonomics Datalog Tx: <a
                    :href="makeSubscanLink(datalogTxId)"
                    class="text-yellow-500"
                    target="_blank"
                    rel="noopener noreferrer"
                  >{{ addressShort(datalogTxId) }}</a>
                </p>
                <p class="text-md mt-2 text-white">
                  Crust Storage Order Tx: <a
                    :href="makeSubscanLink('crust', crustTxId)"
                    class="text-yellow-500"
                    target="_blank"
                    rel="noopener noreferrer"
                  >{{ addressShort(crustTxId) }}</a>
                </p>
              </CardContainer>
              <CardContainer v-if="launchData" title="Video Record">
                <video :src="`${makeIpfsFolderLink(traceInfo)}/h264_camera.mp4`" type="video/mp4" controls />
              </CardContainer>

              <CardContainer v-if="launchData" title="Digital twin">
                <RosbagPlayer :rosbag-url="`${makeIpfsFolderLink(traceInfo)}/state.bag`" />
              </CardContainer>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import { defineComponent, onMounted, useRoute, ref } from '@nuxtjs/composition-api'
import { readRobonomicsLaunchTracesBySender } from '../../plugins/merklebot'
import { makeSubscanLink } from '~/plugins/robonomics'

export default defineComponent({
  setup () {
    const route = useRoute()
    const txId = route.value.params.record

    const launchData = ref(null)
    const traceInfo = ref(null)
    const launchTxId = ref(null)
    const datalogTxId = ref(null)
    const crustTxId = ref(null)

    if (!txId) {
      return {
        txId: null
      }
    }

    onMounted(async () => {
      const res = await readRobonomicsLaunchTracesBySender({ launchTxId: txId })
      console.log(res)
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
    })

    const addressShort = (address) => {
      if (!address) {
        return ''
      }
      return address.slice(0, 6) + '...' + address.slice(-4)
    }

    const makeIpfsFolderLink = ({ ipfsCid, sender, nonce, createdAt }) => {
      return `https://merklebot.mypinata.cloud/ipfs/${ipfsCid}/spot/spot.merklebot.com/spot/traces/user-${sender}-cps-4FNQo2tK6PLeEhNEUuPePs8B8xKNwx15fX7tC2XnYpkC8W1j-session-${nonce}-${createdAt}`
    }

    return {
      txId, launchData, traceInfo, launchTxId, datalogTxId, crustTxId, addressShort, makeSubscanLink, makeIpfsFolderLink
    }
  }
})

</script>
