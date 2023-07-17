import { Contract } from '@ethersproject/contracts'
import { formatEther, formatUnits } from '@ethersproject/units'
import { useWeb3 } from '@instadapp/vue-web3'
import { watch } from '@nuxtjs/composition-api'
import { defineStore } from 'pinia'
import xrtAbi from '../abi/xrt.json'
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
      const { library, chainId } = useWeb3()
      this.selectedAccount.account = { address: account }

      watch([account, library, chainId], () => {
        if (!!library.value && !!account.value) {
          library.value
            .getBalance(account.value)
            .then((value) => {
              this.selectedAccount.balanceRaw = value
              this.selectedAccount.balanceFormatted = formatEther(value) + ' XRT'
            })
            .catch(() => {})
        }
      })

      const xrtAddress = '0x7dE91B204C1C737bcEe6F000AAA6569Cf7061cb7'
      const contract = new Contract(xrtAddress, xrtAbi, library.value)
      setInterval(async () => {
        const balance = await contract.balanceOf(account.value)
        this.selectedAccount.balanceRaw = balance
        this.selectedAccount.balanceFormatted = formatUnits(balance, 9) + ' XRT'
      }, 3000)
    }
  }
})
