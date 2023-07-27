import { parseUnits } from '@ethersproject/units'
import { useWeb3 } from '@instadapp/vue-web3'
import awaitTransactionMined from 'await-transaction-mined'
import axios from 'axios'
import { base58_to_binary as base58Encode } from 'base58-js'
import Hash from 'ipfs-only-hash'
import { defineStore } from 'pinia'
import utils from 'web3-utils'
import factoryAbi from '../abi/factory.json'
import liabilityAbi from '../abi/liability.json'
import nftAbi from '../abi/nft.json'
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

function setPrefix (hash) {
  return utils.soliditySha3(
    {
      type: 'bytes',
      value: utils.stringToHex('\x19Ethereum Signed Message:\n32')
    },
    { type: 'bytes', value: hash }
  )
}

async function demand (library, account, objective) {
  const factoryContract = new library.eth.Contract(factoryAbi, factoryAddress)
  const nonce = await factoryContract.methods.nonceOf(account).call()
  const block = await library.eth.getBlockNumber()
  const demandData =
  {
    model: utils.bytesToHex(base58Encode(model)),
    objective: library.utils.toHex(objective),
    token: xrtAddress,
    cost: parseUnits('1', 9).toNumber(),
    lighthouse: lighthouseAddress,
    validator: validatorAddress,
    validatorFee: 0,
    deadline: block + 1000,
    nonce: Number(nonce.toString()),
    sender: account,
    signature: ''
  }
  const hash = demandHash(demandData)
  demandData.signature = await library.eth.sign(setPrefix(hash), account)
  return demandData
}

async function getPromisee (library, address) {
  const liability = new library.eth.Contract(liabilityAbi, address)
  return await liability.methods.promisee().call()
}
async function getResult (library, address) {
  const liability = new library.eth.Contract(liabilityAbi, address)
  return await liability.methods.result().call()
}
async function getApprove (library, account) {
  const xrtContract = new library.eth.Contract(xrtAbi, xrtAddress)
  return await xrtContract.methods.allowance(account, factoryAddress).call()
}
async function approve (library, value, account) {
  const xrtContract = new library.eth.Contract(xrtAbi, xrtAddress)
  const tx = await xrtContract.methods.approve(factoryAddress, value).send({ from: account })
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
        queue: null,
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
        },
        nft: { contract: null, tokenId: null }
      }
    }
  },
  actions: {
    async launchCps (transferXrtAmount, commandParams) {
      this.cps.launch.txInfo = { tx: null }
      this.cps.launch.txStatus = null
      this.cps.approve = { status: false, tx: null }
      this.cps.liability = { address: null, result: false }
      this.cps.nft = { contract: null, tokenId: null }
      this.cps.queue = null

      const commandParamsJSON = JSON.stringify(commandParams)
      const commandParamsHash = await Hash.of(commandParamsJSON)
      await uploadCommandParamsToIpfs(commandParamsJSON)

      console.log(commandParamsHash)
      console.log(commandParamsJSON)

      const { library, account } = useWeb3()

      const allowance = await getApprove(library.value, account.value)
      if (Number(allowance) < parseUnits('1', 9).toNumber()) {
        const tx = await approve(library.value, parseUnits('100', 9), account.value)
        this.cps.approve.tx = tx.transactionHash
        await awaitTransactionMined.awaitTx(library.value, tx.transactionHash, { blocksToWait: 12 })
        this.cps.approve.status = true
      } else {
        this.cps.approve.status = true
      }

      const getTokenInfo = async (library, address, id) => {
        const nftContract = new library.eth.Contract(nftAbi, address)
        const nftUri = await nftContract.methods.tokenURI(id).call()
        const nftData = (await axios.get(nftUri)).data
        this.nftData = nftData
      }
      const checkNftToken = async (library, address, id) => {
        const nftContract = new library.eth.Contract(nftAbi, address)
        return await nftContract.methods.ownerOf(id).call()
      }

      const ipfs = getIpfs()

      const demandMsg = await demand(library.value, account.value, commandParamsHash)

      const handler = async (r) => {
        if (r.from === ipfsSender) {
          const msgResponse = decodeMsg(r.data)

          console.log(msgResponse)

          if (msgResponse.liability) {
            const p = await getPromisee(library.value, msgResponse.liability)
            console.log({ liability: msgResponse.liability, p })
          }
          if (msgResponse.finalized && this.cps.liability.address) {
            const res = await getResult(library.value, this.cps.liability.address)
            console.log({ finalized: true, liability: this.cps.liability.address, res })
          }

          if (msgResponse.queue && msgResponse.sender === demandMsg.sender && msgResponse.nonce === demandMsg.nonce) {
            this.cps.queue = msgResponse.queue
          }

          if (
            (msgResponse.gotDemand && msgResponse.demandSender === account.value && msgResponse.demandObjective === demandMsg.objective) ||
            (msgResponse.objective === demandMsg.objective && msgResponse.sender === demandMsg.sender)
          ) {
            console.log('stop reapeat publish')
            clearInterval(intervalPublish)
          }
          if (msgResponse.liability && await getPromisee(library.value, msgResponse.liability) === account.value) {
            this.cps.liability.address = msgResponse.liability
          }
          if (msgResponse.nftContract && this.cps.liability.address === msgResponse.liabilityAddress) {
            const owner = await checkNftToken(library.value, msgResponse.nftContract, msgResponse.tokenId)
            console.log({ nftowner: owner })
            if (owner === account.value) {
              this.cps.nft.contract = msgResponse.nftContract
              this.cps.nft.tokenId = msgResponse.tokenId
              getTokenInfo(library.value, msgResponse.nftContract, msgResponse.tokenId)
            }
          }
          if (msgResponse.finalized && this.cps.liability.address && await getResult(library.value, this.cps.liability.address)) {
            this.cps.liability.result = msgResponse.finalized
            ipfs.pubsub.unsubscribe(topic, handler)
          }
        }
      }

      ipfs.pubsub.subscribe(topic, handler, { discover: true })

      ipfs.pubsub.publish(topic, encodeMsg(demandMsg))
      let count = 1
      const intervalPublish = setInterval(() => {
        if (count >= 10) {
          console.log('stop reapeat publish. max count')
          clearInterval(intervalPublish)
          return
        }
        console.log('repeat publish')
        ipfs.pubsub.publish(topic, encodeMsg(demandMsg))
        count++
      }, 3000)

      this.cps.status = 'wait_tx'
      this.cps.launch.txStatus = 'accepted'
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
