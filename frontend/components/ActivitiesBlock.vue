<template>
  <div class="bg-gray-800 flex">
    <div
      class="overflow-x-hidden overflow-y-auto snap-y snap-mandatory"
    >
      <ProgressContainer>
        <ProgressContainerElement title="Connect your wallet" :status="progressElementStatuses['connectWallet']">
          <StepContentContainer>
            <Anchor anchor-id="anchor-to-1" href-id="#1" title="" />

            <p class="text-md my-2 text-white mx-6">
              Identity and access rights are managed using the cryptographic key
              from your Web3 wallet.
            </p>
            <img src="pictures/Frame2.png">
            <div class="flex items-center justify-center">
              <Account />
              <AccountConnector />
            </div>
            <div>
              <p class="text-md mt-2 text-white text-center">
                Ipfs pubsub: <span class="text-yellow-500">{{ ipfs.peers.length > 0 ? 'success' : 'waiting' }}</span>
              </p>
            </div>
          </StepContentContainer>
        </ProgressContainerElement>

        <ProgressContainerElement title="Acquire launch rights" :status="progressElementStatuses['transferValue']">
          <StepContentContainer>
            <Anchor anchor-id="anchor-to-2" href-id="#2" title="" />
            <p class="text-md my-2 text-white mx-6">
              To make onboarding easier for our clients billing can be done in both US dollars and cryptocurrencies - money for robots.
            </p>
            <img src="pictures/Frame3.png">
            <p class="text-md my-2 text-white mx-6">
              One launch requires 1 XRT.
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

        <ProgressContainerElement title="Wait for Spot to draw your picture" :status="progressElementStatuses['waitTx']">
          <Anchor anchor-id="anchor-to-5" href-id="#5" title="" />
          <StepContentContainer>
            <DashboardLikeContainer>
              <LaunchTransactionInfoCard />
              <RobotStateCard />
              <SpotAnimation />
            </DashboardLikeContainer>
          </StepContentContainer>
        </ProgressContainerElement>

        <ProgressContainerElement title="Here is the result of your collaboration with Spot!" :status="progressElementStatuses['recordedData']">
          <StepContentContainer>
            <Anchor anchor-id="anchor-to-8" href-id="#8" title="" />
            <ResultingRecordCard />
          </StepContentContainer>
        </ProgressContainerElement>

        <ProgressContainerElement title="" status="wait">
          <StepContentContainer>
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
import { computed, defineComponent } from '@nuxtjs/composition-api'

import DashboardLikeContainer from '~/components/DashboardLikeContainer'
import ProgressContainerElement from '~/components/ProgressContainerElement'
import RobotStateCard from '~/components/RobotStateCard'
import { useDAppParameters } from '~/store'
import { useIpfs } from '~/store/ipfs'
import { useRobot } from '~/store/robot'
import { useWallet } from '~/store/wallet'

export default defineComponent({
  components: {
    DashboardLikeContainer,
    RobotStateCard,
    ProgressContainerElement
  },
  setup () {
    const wallet = useWallet()
    const robot = useRobot()
    const dAppParameters = useDAppParameters()
    const ipfs = useIpfs()

    const progressElementStatuses = computed(() => {
      const hasEnoughXrt = (wallet.selectedAccount.balanceRaw * 10 ** -9 > 1)
      const hasTicket = (wallet.selectedAccount.tickets.filter(ticket => ticket.spent === false).length >= 1)

      const checkPeers = ipfs.peers.includes('QmdfQmbmXt6sqjZyowxPUsmvBsgSGQjm4VXrV7WGy62dv8') ||
        ipfs.peers.includes('QmPTFt7GJ2MfDuVYwJJTULr6EnsQtGVp8ahYn9NSyoxmd9') ||
        ipfs.peers.includes('QmWZSKTEQQ985mnNzMqhGCrwQ1aTA6sxVsorsycQz9cQrw')

      const stagesStatus = {
        connectWallet: (wallet.walletConnectionStatus === 'connected') && checkPeers,
        transferValue: ((hasEnoughXrt || hasTicket) || (robot.cps.launch.txStatus !== null)),
        draw: ((dAppParameters.currentDrawingSegments.length > 0) || (robot.cps.launch.txStatus !== null)),
        sendLaunchCommand: (robot.cps.status !== 'unknown'),
        waitTx: (robot.cps.launch.txStatus === 'accepted'),
        recordedData: (robot.cps.nft !== null)
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
    })

    return { wallet, progressElementStatuses, ipfs }
  }
})
</script>
