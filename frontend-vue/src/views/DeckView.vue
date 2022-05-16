<template>
  <h1>Deck</h1>
  <span>
    <h2>Select account</h2>
    <form>
      <select v-model="selectedAccount.account">
        <option v-for="(account, idx) in accounts" :key="idx" :value="account">
          {{ account.meta?.source }} - {{ account.meta.name }} -
          {{ addressShort(account.address) }}
        </option>
      </select>
    </form>
    <p v-if="selectedAccount.account">
      Balance: {{ selectedAccount.balanceFormatted }}
    </p>
  </span>
  <span>
    <h2>Launch the robot</h2>
    <button @click="launchCps" :disabled="selectedAccount.balanceRaw <= 0">
      Launch
    </button>
    <ul style="list-style: none; padding: 0">
      <li>Robot status: {{ this.cps.status }}</li>
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
          >{{ addressShort(cps.launch.txInfo.tx) }}</a
        >
      </li>
    </ul>
  </span>
</template>

<script>
import {
  getAccounts,
  setActiveAccount,
  subscribeToBalanceUpdates,
  getInstance as getRobonomics,
  makeLaunchTx,
  signAndSendTxWithActiveAccount,
} from "@/plugins/robonomics";
import { formatBalance } from "@polkadot/util";

export default {
  data() {
    return {
      accounts: [],
      selectedAccount: {
        account: null,
        balanceRaw: null,
        balanceFormatted: null,
      },
      cps: {
        address: "4FNQo2tK6PLeEhNEUuPePs8B8xKNwx15fX7tC2XnYpkC8W1j",
        status: "unknown",
        launch: {
          txInfo: null,
          txStatus: null,
        },
      },
    };
  },
  mounted() {
    getAccounts().then((accounts) => {
      this.accounts = accounts;
      this.selectedAccount.account = accounts[0];
    });
  },
  methods: {
    addressShort(address) {
      return address.slice(0, 6) + "..." + address.slice(-4);
    },
    async launchCps() {
      const launchTx = await makeLaunchTx(this.cps.address, true);
      this.cps.launch.txInfo = await signAndSendTxWithActiveAccount(launchTx);
      this.cps.launch.txStatus = "accepted";
      this.cps.status = "activated";
    },
  },
  watch: {
    "selectedAccount.account": function (account) {
      setActiveAccount(account.address);
      subscribeToBalanceUpdates(this.selectedAccount.account.address, (r) => {
        getRobonomics().then((robonomics) => {
          const balance = r.free.sub(r.feeFrozen);
          this.selectedAccount.balanceRaw = balance;
          this.selectedAccount.balanceFormatted = formatBalance(balance, {
            decimals: robonomics.api.registry.chainDecimals[0],
            withUnit: robonomics.api.registry.chainTokens[0],
          });
        });
      });
    },
  },
};
</script>
