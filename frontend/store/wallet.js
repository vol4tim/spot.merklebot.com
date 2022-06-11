import { defineStore } from 'pinia'
import { formatBalance } from '@polkadot/util'
import { readTicketsByCustomer } from '../plugins/merklebot'
import {
  getAccounts,
  setActiveAccount,
  subscribeToBalanceUpdates,
  getInstance as getRobonomics

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

      subscribeToBalanceUpdates(this.selectedAccount.account.address, (r) => {
        getRobonomics().then((robonomics) => {
          const balance = r.free.sub(r.feeFrozen)
          this.selectedAccount.balanceRaw = balance
          if (balance === 0) {
            this.selectedAccount.balanceFormatted = '0 XRT'
          }
          this.selectedAccount.balanceFormatted = formatBalance(balance, {
            decimals: robonomics.api.registry.chainDecimals[0],
            withUnit: robonomics.api.registry.chainTokens[0]
          })
          readTicketsByCustomer(account.address).then((tickets) => { this.selectedAccount.tickets = tickets })
        })
      })
    }
  }
})
