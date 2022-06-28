<template>
  <div class="flex">
    <div
      class="overflow-x-hidden overflow-y-auto h-screen snap-y snap-mandatory"
    >
      <ProgressContainer>
        <ProgressContainerElement title="Connect you wallet" :status="progressElementStatuses['connectWallet']">
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
                >Polkadot.js extension</a>, create and add Web3 account. Then reload this page. -->
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

        <ProgressContainerElement title="Get robot's transfer value" :status="progressElementStatuses['transferValue']">
          <StepContentContainer>
            <Anchor anchor-id="anchor-to-2" href-id="#2" title="" />

            <p class="text-md my-2 text-white mx-6">
              Billing for robot’s work can happen in both US dollars and
              cryptocurrencies - money for robots.
            </p>
            <img src="/pictures/Frame3.png">

            <PurchaseTicket class="mt-4 mx-6 pr-16 w-full" />
          </StepContentContainer>
        </ProgressContainerElement>

        <ProgressContainerElement title="Draw something" :status="progressElementStatuses['draw']">
          <StepContentContainer>
            <Anchor anchor-id="anchor-to-3" href-id="#3" title="" />
            <p class="text-md my-2 text-white mx-6">
              Now you can collaborate with Spot, draw anything in the box and ask
              her to repeat it:
            </p>

            <div class="flex items-center justify-center mt-4">
              <DrawingPanel :canvas-id="'canvas-one'" />
            </div>
          </StepContentContainer>
        </ProgressContainerElement>

        <ProgressContainerElement title="Send launch transaction" :status="progressElementStatuses['sendLaunchCommand']">
          <StepContentContainer>
            <Anchor anchor-id="anchor-to-4" href-id="#4" title="" />
            <p class="text-md my-2 text-white mx-6">
              Teleoperation session is authorized by the key in your wallet and
              the data can be encrypted with it too.
            </p>
            <img src="/pictures/Frame4.png">

            <div class="flex items-center justify-center mt-4">
              <SendDrawingCommand />
            </div>
          </StepContentContainer>
        </ProgressContainerElement>

        <ProgressContainerElement title="Wait your transaction processing" :status="progressElementStatuses['waitTx']">
          <Anchor anchor-id="anchor-to-5" href-id="#5" title="" />
          <StepContentContainer>
            <DashboardLikeContainer>
              <LaunchTransactionInfoCard />
            </DashboardLikeContainer>
          </StepContentContainer>
        </ProgressContainerElement>

        <ProgressContainerElement title="Follow command execution" :status="progressElementStatuses['robotExecution']">
          <Anchor anchor-id="anchor-to-4" href-id="#6" title="" />
          <StepContentContainer>
            <DashboardLikeContainer>
              <RobotStateCard />
              <SpotAnimation />
            </DashboardLikeContainer>
          </StepContentContainer>
        </ProgressContainerElement>

        <ProgressContainerElement title="See recorded data" :status="progressElementStatuses['recordedData']">
          <StepContentContainer>
            <Anchor anchor-id="anchor-to-7" href-id="#7" title="" />

            <img src="/pictures/Frame5.png">
            <p class="text-md my-2 text-white mx-6">
              Here is a report from your interaction with Spot:
            </p>
            <ResultingRecordCard />
          </StepContentContainer>
        </ProgressContainerElement>

        <ProgressContainerElement title="Read more" status="wait">
          <StepContentContainer>
            <Anchor anchor-id="anchor-to-8" href-id="#8" title="Digital Economies Powering Physical World" />
            <p class="text-md my-2 text-white mx-6">
              With the rise of cryptocurrencies adoption new digital market
              flourished and they present a number of opportunities to reduce
              costs, drive additional revenue streams and partnerships.
            </p>
            <div class="flex flex-row mx-8 py-4">
              <div class="basis-1/3 mx-2 px-2 bg-gray-600 relative">
                <h4
                  class="max-w-sm mt-4 text-md md:text-xl font-bold text-white"
                >
                  DeFi pools and DAOs (costs 📉)
                </h4>
                <p class="text-md my-4 mb-16 text-white">
                  Data-driven leasing model unlocks global funding sources for new
                  robotics deployments.
                </p>
                <a
                  href="https://docs.google.com/presentation/d/1iMaQJuA91D2bHG1LefyikUMNoGKSNqsXwCDAjztJ9xw/edit?usp=sharing"
                  target="_blank"
                  class="
                  absolute bottom-0 inset-x-0 uppercase py-2 mx-4 my-2 px-4 md:mt-16
                  text-md text-center
                  text-gray-800 bg-gray-200 border-2
                  hover:bg-gray-100 hover:bg-gray-800 hover:text-white
                "
                >
                  Case study
                </a>
              </div>

              <div class="basis-1/3 mx-2 px-2 bg-gray-600 relative">
                <h4
                  class="max-w-sm text-md md:text-xl font-bold text-white mt-4"
                >
                  NFT and data markets (revenue 📈)
                </h4>
                <p class="text-md my-4 mb-16 text-white">
                  The birth of digital markets present unique opportunities to
                  form supporting community around equipment operators.
                </p>

                <a
                  href="https://telescope.merklebot.com/#/"
                  target="_blank"
                  class="
                  absolute bottom-0 inset-x-0 uppercase py-2 mx-4 my-2 px-4 md:mt-16
                  text-md text-center
                  text-gray-800 bg-gray-200 border-2
                  hover:bg-gray-100 hover:bg-gray-800 hover:text-white
                "
                >
                  Check dApp
                </a>
              </div>
              <div class="basis-1/3 mx-2 px-2 bg-gray-600 relative">
                <h4
                  class="max-w-sm text-md md:text-xl font-bold text-white mt-4"
                >
                  Plug-and-play integrations (optimization 📊)
                </h4>
                <p class="text-md my-4 mb-16 text-white">
                  Open infrastructure and wide hardware support opens endless
                  opportunities for data-driven partnerships and collaboration.
                </p>

                <a
                  href="https://docs.google.com/presentation/d/1iMaQJuA91D2bHG1LefyikUMNoGKSNqsXwCDAjztJ9xw/edit?usp=sharing"
                  target="_blank"
                  class="
                  absolute bottom-0 inset-x-0 uppercase py-2 mx-4 my-2 px-4 md:mt-16
                  text-md text-center
                  text-gray-800 bg-gray-200 border-2
                  hover:bg-gray-100 hover:bg-gray-800 hover:text-white
                "
                >
                  Case study
                </a>
              </div>
            </div>
            <p class="text-white mx-6">
              To learn more send us an email to
              <span class="text-orange-600 font-bold">v@merklebot.com</span>.
            </p>
          </StepContentContainer>
        </ProgressContainerElement>
      </ProgressContainer>
    </div>
  </div>
</template>

<script>
import { defineComponent } from '@vue/composition-api'
import { computed } from '@nuxtjs/composition-api'

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

    return { wallet, progressElementStatuses }
  }
})
</script>
