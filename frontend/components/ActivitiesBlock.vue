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
          </StepContentContainer>
        </ProgressContainerElement>
        <ProgressContainerElement v-if="wallet.selectedAccount.account && wallet.selectedAccount.tickets.length===0" title="Get your free ticket" :status="progressElementStatuses['connectWallet']">
          <StepContentContainer>
            <Anchor anchor-id="anchor-to-1" href-id="#1" title="" />

            <p class="text-md my-2 text-white mx-6">
              As a part of this demo we demonstrate the billing system for robotics. If you leave your email below — your first demo is on us!
            </p>
            <UserInfoSurveyWrapper @complete="openModal" />
            <div
              class="text-sm mt-4 text-white"
            >
              * we never store your email and wallet info together, we’ll use your email to send you info about Web3 and robotics.
            </div>
          </StepContentContainer>
        </ProgressContainerElement>

        <ProgressContainerElement title="Acquire launch rights" :status="progressElementStatuses['transferValue']">
          <StepContentContainer>
            <Anchor anchor-id="anchor-to-2" href-id="#2" title="" />

            <p class="text-md my-2 text-white mx-6">
              To make onboarding easier for our clients billing can be done in both US dollars and cryptocurrencies - money for robots.
            </p>
            <img src="/pictures/Frame3.png">

            <p class="text-md my-2 text-white mx-6">
              One launch requires 1 ticket <em>or</em> 1 XRT.
            </p>
            <PurchaseTicket class="mt-4 mx-6 pr-16 w-full" />
          </StepContentContainer>
        </ProgressContainerElement>

        <ProgressContainerElement title="Draw something" :status="progressElementStatuses['draw']">
          <StepContentContainer>
            <Anchor anchor-id="anchor-to-3" href-id="#3" title="" />
            <p class="text-md my-2 text-white mx-6">
              Now you can collaborate with Spot, draw anything in the box and our robodog will trace your art in the air:
            </p>

            <div class="flex items-center justify-center mt-4">
              <DrawingPanel :canvas-id="'canvas-one'" />
            </div>
            <div>
              <p class="text-md my-2 text-white mx-6">
                Teleoperation is authorized by sending a transaction directly to the robot using either a ticket or XRT token.
              </p>

              <div class="flex items-center justify-center mt-4">
                <SendDrawingCommand />
              </div>
            </div>
          </StepContentContainer>
        </ProgressContainerElement>

        <!--        <ProgressContainerElement title="Send launch transaction" :status="progressElementStatuses['sendLaunchCommand']">-->
        <!--          <StepContentContainer>-->
        <!--            <Anchor anchor-id="anchor-to-4" href-id="#4" title="" />-->
        <!--            <p class="text-md my-2 text-white mx-6">-->
        <!--              Teleoperation is authorized by sending a transaction directly to the robot using either a ticket or XRT token.-->
        <!--            </p>-->
        <!--            &lt;!&ndash;            <img src="/pictures/Frame4.png">&ndash;&gt;-->

        <!--            <div class="flex items-center justify-center mt-4">-->
        <!--              <SendDrawingCommand />-->
        <!--            </div>-->
        <!--          </StepContentContainer>-->
        <!--        </ProgressContainerElement>-->

        <ProgressContainerElement title="Wait for your transaction to process" :status="progressElementStatuses['waitTx']">
          <Anchor anchor-id="anchor-to-5" href-id="#5" title="" />
          <StepContentContainer>
            <DashboardLikeContainer>
              <LaunchTransactionInfoCard />
            </DashboardLikeContainer>
          </StepContentContainer>
        </ProgressContainerElement>

        <ProgressContainerElement title="Watch Spot draw in the air" :status="progressElementStatuses['robotExecution']">
          <Anchor anchor-id="anchor-to-4" href-id="#6" title="" />
          <StepContentContainer>
            <DashboardLikeContainer>
              <RobotStateCard />
              <SpotAnimation />
            </DashboardLikeContainer>
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

        <ProgressContainerElement title="Learn more" status="wait">
          <StepContentContainer>
            <Anchor anchor-id="anchor-to-8" href-id="#8" title="" />
            <p class="mx-6 text-white text-md">
              Digital economies will soon power our physical world and they present a number of
              opportunities for robotics developers and operators to reduce costs, drive additional
              revenue streams and partnerships.
            </p>
            <div class="mx-6">
              <div class="w-full my-8">
                <h4 class="w-full text-md md:text-xl font-bold text-white">
                  Equipment financing with DeFi pools (costs📉)
                </h4>
                <p class="my-4 text-md text-white">
                  Data-driven leasing model derisks equipment financing and we unlock new funding
                  source for robotics deployments.
                </p>
                <a
                  href="https://medium.com/merklebot/southie-autonomy-case-study-1633a07dbf2c"
                  target="_blank"
                  class="w-full py-2 my-2 px-4 md:mt-16 uppercase text-md text-center text-gray-800 bg-gray-200 border-2
                    hover:bg-gray-100 hover:bg-gray-800 hover:text-white"
                >
                  Case study
                </a>
              </div>
              <div class="w-full my-8">
                <h4 class="w-full text-md md:text-xl font-bold text-white">
                  New revenue via NFTs (revenue📈)
                </h4>
                <p class="my-4 text-md text-white">
                  By connecting an autonomous telescope in Chile and allowing it to mint NFTs we
                  support local astronomers community.
                </p>
                <a
                  href="https://telescope.merklebot.com/#/"
                  target="_blank"
                  class="w-full py-2 my-2 px-4 md:mt-16 uppercase text-md text-center text-gray-800 bg-gray-200 border-2
                    hover:bg-gray-100 hover:bg-gray-800 hover:text-white"
                >
                  Visit dApp
                </a>
              </div>
              <div class="w-full my-8">
                <h4 class="w-full text-md md:text-xl font-bold text-white">
                  Partnerships (optimization📊)
                </h4>
                <p class="my-4 text-md text-white">
                  Easy plug-and-play integrations with parachains in PolkadotService ecosystem create endless opportunities for improving internal processes in robotics and equipment operations via Robonomics.
                </p>
                <a
                  href="https://robonomics.network/blog/release-2-0-and-xcm-support/"
                  target="_blank"
                  class="w-full py-2 my-2 px-4 md:mt-16 uppercase text-md text-center text-gray-800 bg-gray-200 border-2
                    hover:bg-gray-100 hover:bg-gray-800 hover:text-white"
                >
                  Case study
                </a>
              </div>
            </div>
            <p class="text-white mx-6">
              <a
                href="https://discord.gg/7u8MdtuaX2"
                target="_blank"
                rel="noopener noreferrer"
              >
                <img class="max-w-[30px] inline" src="~/assets/discord.png">
                <div class="inline text-orange-500 underline">
                  Join our Discord to learn more.
                </div>
              </a>
            </p>
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
import { useDAppParameters } from '~/store'
import ProgressContainerElement from '~/components/ProgressContainerElement'
import RobotStateCard from '~/components/RobotStateCard'
import DashboardLikeContainer from '~/components/DashboardLikeContainer'

export default defineComponent({
  components: { DashboardLikeContainer, RobotStateCard, ProgressContainerElement },
  setup () {
    const wallet = useWallet()
    const robot = useRobot()
    const dAppParameters = useDAppParameters()
    const modal = ref()
    const openModal = () => {
      modal.value.openModal()
    }

    const progressElementStatuses = computed(() => {
      const hasEnoughXrt = (wallet.selectedAccount.balanceRaw * 10 ** -9 > 1)
      const hasTicket = (wallet.selectedAccount.tickets.filter(ticket => ticket.spent === false).length >= 1)

      const stagesStatus = {
        connectWallet: (wallet.walletConnectionStatus === 'connected'),
        transferValue: ((hasEnoughXrt || hasTicket) || (robot.cps.launch.txStatus !== null)),
        draw: ((dAppParameters.currentDrawingSegments.length > 0) || (robot.cps.launch.txStatus !== null)),
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

    return { wallet, progressElementStatuses, modal, openModal }
  }
})
</script>
