import { Contract } from '@ethersproject/contracts'
import { formatUnits } from '@ethersproject/units'
import { useWeb3 } from '@instadapp/vue-web3'
import { watch } from '@nuxtjs/composition-api'
import { defineStore } from 'pinia'
import xrtAbi from '../abi/xrt.json'
import { xrtAddress } from '../connectors/config'
import { readTicketsByCustomer } from '../plugins/merklebot'

export const useWallet = defineStore('wallet', {
  state: () => {
    return {
      accounts: [],
      walletConnectionStatus: 'wait',
      selectedAccount: {
        account: null,
        balanceRaw: null,
        balanceFormatted: null,
        tickets: []

      }
    }
  },
  actions: {
    connectWallet () {
      const { account, active } = useWeb3()
      watch([active], () => {
        if (active.value) {
          this.setActiveAccount(account)
          this.walletConnectionStatus = 'connected'
        }
      })
    },
    async updateTicketsList () {
      if (this.selectedAccount.account) {
        this.selectedAccount.tickets = await readTicketsByCustomer(this.selectedAccount.account.address)
      }
    },
    setActiveAccount (account) {
      const { library } = useWeb3()
      this.selectedAccount.account = { address: account }

      const contract = new Contract(xrtAddress, xrtAbi, library.value)
      const getBalance = async () => {
        const balance = await contract.balanceOf(account.value)
        this.selectedAccount.balanceRaw = balance
        this.selectedAccount.balanceFormatted = formatUnits(balance, 9) + ' XRT'
      }
      getBalance()
      setInterval(getBalance, 3000)
    }
  }
})
