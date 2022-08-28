<template>
  <div class="flex">
    <div
      class="overflow-x-hidden overflow-y-auto snap-y snap-mandatory"
    >
      <Modal ref="modal" />
      <ProgressContainer>
        <ProgressContainerElement title="Connect your wallet" :status="progressElementStatuses['connectWallet']">
          <StepContentContainer>
            <Anchor anchor-id="anchor-to-1" href-id="#1" title="" />

            <p class="text-md my-2 text-white mx-6">
              Identity and access rights are managed using the cryptographic key
              from your Web3 wallet.
            </p>
            <img src="/pictures/Frame2.png">
            <div class="flex items-center justify-center">
              <AccountChooser />
              <div v-if="wallet.walletConnectionStatus === 'error'">
                <p class="text-xl my-6 text-center text-white font-bold">
                  ❗ Please install
                  <!-- <a
                  class="text-orange-600"
                  href="https://polkadot.js.org/extension/"
                  target="_blank"
                >PolkadotService.js extension</a>, create and add Web3 account. Then reload this page. -->
                  <a
                    class="text-orange-600"
                    href="https://talisman.xyz/"
                    target="_blank"
                  >Talisman web3 wallet</a> and create an account. Then reload this page.
                </p>
              </div>
            </div>
            <div>
              <p class="text-md my-2 text-white mx-6">
                You need to get your control token by signing robot's token
              </p>

              <button
                type="button"
                class="uppercase text-md w-full py-2 my-2 px-4 bg-gray-200 text-gray-800
        hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
                @click="signToken"
              >
                Sign token
              </button>
              <div>status: {{ robot.signedRobotToken?'authed':'not authed' }}</div>
            </div>
          </StepContentContainer>
        </ProgressContainerElement>

        <ProgressContainerElement title="Send launch transaction" :status="progressElementStatuses['sendLaunchCommand']">
          <StepContentContainer>
            <Anchor anchor-id="anchor-to-4" href-id="#4" title="" />
            <p class="text-md my-2 text-white mx-6">
              Teleoperation is authorized by sending transactions directly to the robot’s address using your wallet.
            </p>
            <img src="/pictures/Frame4.png">

            <div class="flex items-center justify-center mt-4">
              <SendDrawingCommand />
            </div>
          </StepContentContainer>
        </ProgressContainerElement>

        <ProgressContainerElement title="Wait for your transaction to process" :status="progressElementStatuses['waitTx']">
          <Anchor anchor-id="anchor-to-5" href-id="#5" title="" />
          <StepContentContainer>
            <DashboardLikeContainer>
              <LaunchTransactionInfoCard />
            </DashboardLikeContainer>
          </StepContentContainer>
        </ProgressContainerElement>

        <ProgressContainerElement title="Control spot" :status="progressElementStatuses['robotExecution']">
          <Anchor anchor-id="anchor-to-4" href-id="#6" title="" />
          <StepContentContainer>
            <DashboardLikeContainer>
              <RobotStateCard />
              <SpotAnimation />
            </DashboardLikeContainer>
            <div class="border-2 border-gray-500 p-4">
              <p class="text-md my-2 text-white">
                Control spot
              </p>
              <WASDController />
            </div>
          </StepContentContainer>
        </ProgressContainerElement>

        <ProgressContainerElement title="Review recorded data" :status="progressElementStatuses['recordedData']">
          <StepContentContainer>
            <Anchor anchor-id="anchor-to-7" href-id="#7" title="" />
            <p class="text-md my-2 text-white mx-6">
              The data is recorded using IPFS and stored with multiple replicas using decentralized Crust Network to guarantee availability and resiliency.
            </p>
            <img src="/pictures/Frame5.png">
            <p class="text-md my-2 text-white mx-6">
              Here is the report from your interaction with Spot:
            </p>
            <ResultingRecordCard />
          </StepContentContainer>
        </ProgressContainerElement>
      </ProgressContainer>
    </div>
  </div>
</template>

<script>
import { computed, defineComponent, ref } from '@nuxtjs/composition-api'

import { useWallet } from '~/store/wallet'
import { useRobot } from '~/store/robot'
import ProgressContainerElement from '~/components/ProgressContainerElement'
import RobotStateCard from '~/components/RobotStateCard'
import DashboardLikeContainer from '~/components/DashboardLikeContainer'
import { getAuthToken } from '~/plugins/camera'
import { signMessage } from '~/plugins/robonomics'

export default defineComponent({
  components: { DashboardLikeContainer, RobotStateCard, ProgressContainerElement },
  setup () {
    const wallet = useWallet()
    const robot = useRobot()
    const modal = ref()
    const openModal = () => {
      modal.value.openModal()
    }

    const signToken = async () => {
      console.log(wallet.selectedAccount.account.address)
      const token = await getAuthToken(wallet.selectedAccount.account.address)
      const signedMessage = await signMessage(token)
      console.log(token)
      console.log(signedMessage)
      robot.robotToken = token
      robot.signedRobotToken = signedMessage
    }

    const progressElementStatuses = computed(() => {
      const stagesStatus = {
        connectWallet: (wallet.walletConnectionStatus === 'connected'),
        sendLaunchCommand: (robot.cps.status !== 'unknown'),
        waitTx: (robot.cps.launch.txStatus === 'accepted'),
        robotExecution: (robot.cps.launch.recordData !== null),
        recordedData: (robot.cps.launch.recordData !== null)
      }

      const resultStatuses = {}
      let lastStatus = 'success'
      Object.keys(stagesStatus).forEach((stage) => {
        if (lastStatus === 'success') {
          const stageStatus = stagesStatus[stage] ? 'success' : 'wait'
          lastStatus = stageStatus
          resultStatuses[stage] = stageStatus
        } else if (lastStatus === 'wait') {
          lastStatus = 'disabled'
          resultStatuses[stage] = 'disabled'
        } else if (lastStatus === 'disabled') {
          resultStatuses[stage] = 'disabled'
        }
      })

      return resultStatuses
    }

    )

    return { wallet, robot, progressElementStatuses, modal, openModal, signToken }
  }
})
</script>
