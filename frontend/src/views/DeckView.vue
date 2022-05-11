<template>Deck</template>

<script>
import {
  getInstance as getRobonomics,
  getAddresses,
  getAccountByAddress,
  setActiveAccount,
} from "@/plugins/robonomics";

export default {
  data() {
    return {
      addresses: [],
      activeAccount: {},
      ready: {
        robonomics: false,
      },
    };
  },
  mounted() {
    getRobonomics()
      .then(() => {
        return getAddresses();
      })
      .then((addresses) => {
        this.addresses = addresses;
        this.activeAccount = { address: this.addresses[0] };
        return setActiveAccount(this.addresses[0]);
      })
      .then(() => {
        return getAccountByAddress(this.activeAccount.address);
      })
      .then((activeAccount) => {
        this.activeAccount = activeAccount;
      });
  },
};
</script>
