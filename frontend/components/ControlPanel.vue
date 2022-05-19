<template>
  <div>
    <span>
      <p>Queued: {{ queueSize }}</p>
      <p>Robot state: {{ robotState }}</p>
      <p v-if="lastSessionId && robotState==='idle'">Last session: <NuxtLink :to="`/records/${lastSessionId}`">{{ lastSessionId }}</NuxtLink></p>

      <button :disabled="false" @click="launchCps">
        Launch
      </button>
      <ul style="list-style: none; padding: 0">
        <li>Robot status: {{ cps.status }}</li>
        <li v-if="cps.launch.txStatus">
          Transaction status: {{ cps.launch.txStatus }}
        </li>
        <li v-if="cps.launch.txInfo">
          View transaction:
          <a
            :href="
              'https://robonomics.subscan.io/extrinsic/' + cps.launch.txInfo.tx
            "
            target="_blank"
            rel="noopener noreferrer"
          >{{ addressShort(cps.launch.txInfo.tx) }}</a>
        </li>
      </ul>
    </span>
  </div>
</template>

<script>

import {
  makeLaunchTx,
  signAndSendTxWithActiveAccount
} from '@/plugins/robonomics'

export default {
  name: 'ControlPanel',
  data () {
    return {
      queueSize: null,
      robotState: null,
      lastSessionId: null,
      selectedAccount: {
        account: null,
        balanceRaw: null,
        balanceFormatted: null
      },
      cps: {
        address: '4FNQo2tK6PLeEhNEUuPePs8B8xKNwx15fX7tC2XnYpkC8W1j',
        status: 'unknown',
        launch: {
          txInfo: null,
          txStatus: null
        }
      }

    }
  },
  mounted () {
    this.doRobotStatePolling()
  },
  methods: {
    async launchCps () {
      this.cps.launch.txInfo = null
      this.cps.launch.txStatus = null
      const launchTx = await makeLaunchTx(this.cps.address, true)
      this.cps.status = 'wait_tx'
      this.cps.launch.txInfo = await signAndSendTxWithActiveAccount(launchTx)
      this.cps.launch.txStatus = 'accepted'
      this.cps.status = 'activated'
    },
    addressShort (address) {
      return address.slice(0, 6) + '...' + address.slice(-4)
    },
    async updateRobotState () {
      // const response = await fetch('http://10.200.0.3:1234/current_state', { method: 'GET' })
      const response = await fetch('https://api.merklebot.com/strelka/current_state', { method: 'GET' })
      const json = await response.json()

      this.robotState = json.robot_state
      this.queueSize = json.queue_size
      this.lastSessionId = json.last_session_id
      return true
    },
    async doRobotStatePolling () {
      await this.updateRobotState()
      setTimeout(this.doRobotStatePolling, 1000)
    }
  }
}
</script>

<style scoped>

</style>
