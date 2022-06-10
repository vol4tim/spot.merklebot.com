<template>
  <main class="bg-gray-100 dark:bg-gray-800 h-screen overflow-hidden relative">
    <div class="flex items-start justify-between">
      <SidePanel active="Records" />
      <div class="flex flex-col w-full md:space-y-4">
        <HeaderPanel />
        <div class="overflow-auto h-screen pb-24 px-4 md:px-6">
          <div v-if="!sessionId">
            <h1 class="text-4xl font-semibold text-gray-800 dark:text-white">
              Sessions
            </h1>
            <div class="grid grid-cols-1 gap-4 my-4">
              <RecordsList />
            </div>
          </div>
          <div v-if="sessionId">
            <h1 class="text-4xl font-semibold text-gray-800 dark:text-white">
              Session {{ sessionId }}
            </h1>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4 my-4">
              <CardContainer title="Session Info">
                <p>IPFS Content ID: {{ sessionData['ipfs_cid'] }}</p>
                <p>View Robonomics Launch Tx: <a :href="datalogLink" class="text-purple-500" target="_blank" rel="noopener noreferrer">{{ launchLink }}</a></p>
                <p>View record data on IPFS: <a :href="traceFolderLink" class="text-purple-500" target="_blank" rel="noopener noreferrer">{{ traceFolderLink.slice(0, 50) + '...' }}</a></p>
                <p>View Robonomics Datalog Tx: <a :href="datalogLink" class="text-purple-500" target="_blank" rel="noopener noreferrer">{{ datalogLink.slice(0, 50) + '...' }}</a></p>
              </CardContainer>
              <CardContainer title="Video Record">
                <video :src="`${traceFolderLink}/h264_camera.mp4`" type="video/mp4" controls />
              </CardContainer>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import RecordsList from '../../components/RecordsList'
export default {
  name: 'RecordPage',
  components: { RecordsList },
  async asyncData ({ route }) {
    const sessionId = route.params.record
    if (!sessionId) {
      return {
        sessionId: null,
        sessionData: null
      }
    }
    const sessionData = await (await fetch('https://api.merklebot.com/robonomics-launch-traces/' + sessionId, { method: 'GET' })).json()
    const traceFolderLink = `https://merklebot.mypinata.cloud/ipfs/${sessionData.ipfs_cid}/spot/davos.merklebot.com/spot/traces/user-${sessionData.sender}-cps-4FNQo2tK6PLeEhNEUuPePs8B8xKNwx15fX7tC2XnYpkC8W1j-session-${sessionData.nonce}-${sessionData.created_at}`
    const launchLink = `https://robonomics.subscan.io/extrinsic/${sessionData.launch_tx_id}`
    const datalogLink = `https://robonomics.subscan.io/extrinsic/${sessionData.datalog_tx_id}`
    return { sessionId, sessionData, traceFolderLink, launchLink, datalogLink }
  }

}
</script>
