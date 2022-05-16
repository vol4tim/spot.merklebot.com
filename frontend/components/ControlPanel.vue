<template>
  <div>
    <span>
      <h2>Launch the robot</h2>
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
  methods: {
    async launchCps () {
      const launchTx = await makeLaunchTx(this.cps.address, true)
      this.cps.status = 'wait_tx'
      this.cps.launch.txInfo = await signAndSendTxWithActiveAccount(launchTx)
      this.cps.launch.txStatus = 'accepted'
      this.cps.status = 'activated'
    },
    addressShort (address) {
      return address.slice(0, 6) + '...' + address.slice(-4)
    }

  }
}
</script>

<style scoped>

</style>
