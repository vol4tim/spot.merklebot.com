import { defineStore } from 'pinia'

export const useIpfs = defineStore('ipfs', {
  state: () => {
    return {
      peers: []
    }
  },
  actions: {
    setPeers (peers) {
      this.peers = peers
    }
  }
})
