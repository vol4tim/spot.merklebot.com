import { Contract } from '@ethersproject/contracts'
import { parseUnits } from '@ethersproject/units'
import { useWeb3 } from '@instadapp/vue-web3'
import { base58_to_binary as base58Encode } from 'base58-js'
import Hash from 'ipfs-only-hash'
import { defineStore } from 'pinia'
import utils from 'web3-utils'
import factoryAbi from '../abi/factory.json'
import xrtAbi from '../abi/xrt.json'
import { factoryAddress, ipfsSender, lighthouseAddress, model, topic, validatorAddress, xrtAddress } from '../connectors/config'

import { decodeMsg, encodeMsg, getIpfs } from '~/plugins/ipfs'
import { uploadCommandParamsToIpfs } from '~/plugins/merklebot'

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

async function demand (library, account, objective) {
  const factoryContract = new Contract(factoryAddress, factoryAbi, library)
  const nonce = await factoryContract.nonceOf(account)
  const block = await library.getBlockNumber()
  const demandData =
  {
    model: utils.bytesToHex(base58Encode(model)),
    objective: utils.bytesToHex(base58Encode(objective)),
    token: xrtAddress,
    cost: 1,
    lighthouse: lighthouseAddress,
    validator: validatorAddress,
    validatorFee: 0,
    deadline: block + 1000,
    nonce,
    sender: account,
    signature: ''
  }
  const hash = demandHash(demandData)
  const signer = await library.getSigner()
  demandData.signature = (await signer.signMessage(hash))

  return encodeMsg(demandData)
}

async function getApprove (library, account) {
  const xrtContract = new Contract(xrtAddress, xrtAbi, library)
  return await xrtContract.allowance(account, factoryAddress)
}
async function approve (library, value) {
  const xrtContract = new Contract(xrtAddress, xrtAbi, await library.getSigner())
  const tx = await xrtContract.approve(factoryAddress, value)
  return tx
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
        },
        approve: {
          tx: null,
          status: false
        },
        liability: {
          address: null,
          result: false
        }
      }

    }
  },
  actions: {
    async launchCps (transferXrtAmount, commandParams) {
      this.cps.launch.txInfo = { tx: null }
      this.cps.launch.txStatus = null
      this.cps.approve = { status: false, tx: null }
      this.cps.liability = { address: null, result: false }

      const commandParamsJSON = JSON.stringify(commandParams)
      const commandParamsHash = await Hash.of(commandParamsJSON)
      await uploadCommandParamsToIpfs(commandParamsJSON)

      console.log(commandParamsHash)
      console.log(commandParamsJSON)

      const { library, account } = useWeb3()

      const allowance = await getApprove(library.value, account.value)
      if (allowance.lt(parseUnits('1', 9))) {
        const tx = await approve(library.value, parseUnits('100', 9))
        this.cps.approve.tx = tx.hash
        await tx.wait()
        this.cps.approve.status = true
      } else {
        this.cps.approve.status = true
      }

      const ipfs = getIpfs()

      const handler = (r) => {
        if (r.from === ipfsSender) {
          const msg = decodeMsg(r.data)
          if (msg.liability) {
            this.cps.liability.address = msg.liability
          }
          if (msg.finalized) {
            this.cps.liability.result = true
            ipfs.pubsub.unsubscribe(topic, handler)
          }
        }
      }

      ipfs.pubsub.subscribe(topic, handler, { discover: true })
      const msg = await demand(library.value, account.value, commandParamsHash)
      ipfs.pubsub.publish(topic, msg)
      this.cps.status = 'wait_tx'
      this.cps.launch.txStatus = 'accepted'

      setTimeout(() => {
        ipfs.pubsub.publish(topic, encodeMsg({ liability: '0x123123123' }))
      }, 15000)
      setTimeout(() => {
        ipfs.pubsub.publish(topic, encodeMsg({ finalized: true }))
      }, 20000)

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
      return this.cps.launch
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
