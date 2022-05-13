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
</template>

<script>
import {
  getAccounts,
  setActiveAccount,
  subscribeToBalanceUpdates,
  getInstance as getRobonomics,
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
