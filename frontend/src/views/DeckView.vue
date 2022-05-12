<template>
  <p>Deck</p>
  <p>Addresses: {{ this.addresses }}</p>
</template>

<script>
import { getAddresses } from "@/plugins/robonomics";

export default {
  data() {
    return {
      addresses: [],
    };
  },
  mounted() {
    getAddresses().then((addresses) => {
      this.addresses = addresses;
    });
  },
};
</script>
