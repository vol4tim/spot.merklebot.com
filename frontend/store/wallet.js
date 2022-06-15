import { defineStore } from 'pinia'
import { readTicketsByCustomer } from '../plugins/merklebot'
import {
  getAccounts,
  setActiveAccount,
  subscribeToBalanceUpdates

} from '@/plugins/robonomics'

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
      getAccounts().then((accounts) => {
        console.log('accounts', accounts)
        this.accounts = accounts
        this.setActiveAccount(accounts[0])
        this.walletConnectionStatus = 'connected'
      }).catch((e) => {
        this.walletConnectionStatus = 'error'
      })
    },
    setActiveAccount (account) {
      this.selectedAccount.account = account
      setActiveAccount(account.address)

      subscribeToBalanceUpdates(this.selectedAccount.account.address, ({ free, feeFrozen }) => {
        const balance = free.sub(feeFrozen)
        this.selectedAccount.balanceRaw = balance
        this.selectedAccount.balanceFormatted = (balance * 10 ** -9).toFixed(4) + ' XRT'
        readTicketsByCustomer(account.address).then((tickets) => { this.selectedAccount.tickets = tickets })
      })
    }
  }
})
