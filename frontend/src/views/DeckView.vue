<template>
  <h1>Deck</h1>
  <span>
    <h2>Select account</h2>
    <form>
      <select v-model="selectedAccount">
        <option v-for="(account, idx) in accounts" :key="idx" :value="account">
          {{ account.meta.name }} - {{ addressShort(account.address) }}
        </option>
      </select>
    </form>
  </span>
</template>

<script>
import { getAccounts, setActiveAccount } from "@/plugins/robonomics";

export default {
  data() {
    return {
      accounts: [],
      selectedAccount: null,
    };
  },
  mounted() {
    getAccounts().then((accounts) => {
      this.accounts = accounts;
      this.selectedAccount = accounts[0];
    });
  },
  methods: {
    addressShort(address) {
      return address.slice(0, 6) + "..." + address.slice(-4);
    },
  },
  watch: {
    selectedAccount(account) {
      setActiveAccount(account.address);
    },
  },
};
</script>
