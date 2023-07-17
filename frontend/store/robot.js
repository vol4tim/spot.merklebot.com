import Hash from 'ipfs-only-hash'
import { defineStore } from 'pinia'

import { Contract } from '@ethersproject/contracts'
import { useWeb3 } from '@instadapp/vue-web3'
import utils from 'web3-utils'
import factoryAbi from '../abi/factory.json'

import { uploadCommandParamsToIpfs } from '~/plugins/merklebot'

const xrtAddress = '0x7dE91B204C1C737bcEe6F000AAA6569Cf7061cb7'
const factoryAddress = '0x7e384AD1FE06747594a6102EE5b377b273DC1225'
const lighthouseAddress = '0xD40AC7F1e5401e03D00F5aeC1779D8e5Af4CF9f1'
const validatorAddress = '0x0000000000000000000000000000000000000000'

function demandHash (demand) {
  return utils.soliditySha3(
    { t: 'bytes', v: demand.model },
    { t: 'bytes', v: demand.objective },
    { t: 'address', v: demand.token },
    { t: 'uint256', v: demand.cost },
    { t: 'address', v: demand.lighthouse },
    { t: 'address', v: demand.validator },
    { t: 'uint256', v: demand.validatorFee },
    { t: 'uint256', v: demand.deadline },
    { t: 'uint256', v: demand.nonce },
    { t: 'address', v: demand.sender }
  )
}

function encode (msg) {
  if (msg.signature) {
    msg.signature = msg.signature.replace(/0x/i, '')
  }
  return Buffer.from(JSON.stringify(msg))
}

async function demand (library, account) {
  const factoryContract = new Contract(factoryAddress, factoryAbi, library)
  const nonce = await factoryContract.nonceOf(account)
  const block = await library.getBlockNumber()
  const demandData =
  {
    model: utils.randomHex(34),
    objective: utils.randomHex(34),
    token: xrtAddress,
    cost: 1,
    lighthouse: lighthouseAddress,
    validator: validatorAddress,
    validatorFee: 1,
    deadline: block + 1000,
    nonce,
    sender: account,
    signature: ''
  }
  const hash = demandHash(demandData)
  const signer = await library.getSigner()
  demandData.signature = (await signer.signMessage(hash))

  return encode(demandData)
}

export const useRobot = defineStore('robot', {
  state: () => {
    return {
      robotToken: null,
      signedRobotToken: null,
      queueSize: null,
      robotState: null,
      lastSessionId: null,
      nftData: null,
      cps: {
        address: '4FNQo2tK6PLeEhNEUuPePs8B8xKNwx15fX7tC2XnYpkC8W1j',
        status: 'unknown',
        launch: {
          txInfo: {
            tx: null
          },
          txStatus: null,
          recordData: null
        }
      }

    }
  },
  actions: {
    async launchCps (transferXrtAmount, commandParams) {
      this.cps.launch.txInfo = { tx: null }
      this.cps.launch.txStatus = null
      const commandParamsJSON = JSON.stringify(commandParams)
      const commandParamsHash = await Hash.of(commandParamsJSON)
      await uploadCommandParamsToIpfs(commandParamsJSON)

      console.log(commandParamsHash)
      console.log(commandParamsJSON)

      const { library, account } = useWeb3()
      const msg = await demand(library.value, account.value)
      console.log(msg)

      // const launchTx = await makeLaunchTx(this.cps.address, commandParamsHash)
      // this.cps.status = 'wait_tx'
      // if (transferXrtAmount) {
      //   // const transferTx = await makeTransferTx(this.cps.address, transferXrtAmount)
      //   this.cps.launch.txInfo = await signAndSendTxsBatchWithActiveAccount([launchTx, transferTx])
      // } else {
      //   this.cps.launch.txInfo = await signAndSendTxWithActiveAccount(launchTx)
      // }
      // this.cps.launch.txStatus = 'accepted'
      // this.cps.status = 'activated'
      // return this.cps.launch
    },
    async updateRobotState () {
      // const response = await fetch('http://10.200.0.3:1234/current_state', { method: 'GET' })
      try {
        const response = await fetch('https://api.merklebot.com/strelka/current_state', { method: 'GET' })
        const json = await response.json()
        this.robotState = json.robot_state
        this.queueSize = json.queue_size
        this.lastSessionId = json.last_session_id
        return true
      } catch {
        this.robotState = null
        this.queueSize = null
        this.lastSessionId = null
        return false
      }
    },
    setNftData (data) {
      this.nftData = data
    },
    sendDrawing (account, segments, paymentMode = 'ticket', txId = '') {
      fetch('https://api.merklebot.com/strelka/draw_figure', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          account,
          segments,
          payment_mode: paymentMode,
          tx_id: txId
        })
      }).then(response => response.json()).then((data) => {
        console.log(data)
      })
    },
    startInspection (account = '', paymentMode = 'ticket', txId = '') {
      fetch('https://api.merklebot.com/strelka/start_inspection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          account,
          payment_mode: paymentMode,
          tx_id: txId
        })
      }).then(response => response.json()).then((data) => {
        console.log(data)
      })
    }

  }
})
