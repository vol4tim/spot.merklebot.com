<template>
  <div class="flex">
    <div
      class="overflow-x-hidden overflow-y-auto h-screen snap-y snap-mandatory"
    >
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

        <ProgressContainerElement title="Auth" status="wait">
          <StepContentContainer>
            <Anchor anchor-id="anchor-to-2" href-id="#2" title="" />

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
          </StepContentContainer>
        </ProgressContainerElement>

        <ProgressContainerElement title="Control camera" status="wait">
          <StepContentContainer>
            <Anchor anchor-id="anchor-to-2" href-id="#2" title="" />
            <div class="border-2 border-gray-500 p-4">
              <p class="text-md my-2 text-white">
                Move camera
              </p>
              <div class="grid grid-cols-3 gap-x-4">
                <div />
                <button
                  type="button"
                  class="uppercase text-md w-full py-2 my-2 px-1 bg-gray-200 text-gray-800
        hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
                  @click="()=>moveCommand({x:0, y:1})"
                >
                  Up
                </button>
                <div />
                <button
                  type="button"
                  class="uppercase text-md w-full py-2 my-2 px-1 bg-gray-200 text-gray-800
        hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
                  @click="()=>moveCommand({x:-1, y:0})"
                >
                  Left
                </button>
                <button
                  type="button"
                  class="uppercase text-md w-full py-2 my-2 px-1 bg-gray-200 text-gray-800
        hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
                  @click="()=>moveCommand({x:0, y:-1})"
                >
                  Down
                </button>
                <button
                  type="button"
                  class="uppercase text-md w-full py-2 my-2 px-1 bg-gray-200 text-gray-800
        hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
                  @click="()=>moveCommand({x:1, y:0})"
                >
                  Right
                </button>
              </div>
            </div>
            <div class="border-2 border-gray-500 p-4 mt-4">
              <p class="text-md my-2 text-white">
                Set camera zoom
              </p>
              <div>
                <input v-model="zoomAbsolute" class="border-b-2 border-orange-600 py-2 my-2 px-4 bg-gray-600">
                <button
                  type="button"
                  class="uppercase text-md w-full py-2 my-2 px-4 bg-gray-200 text-gray-800
        hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
                  @click="()=>zoomCommand()"
                >
                  Set zoom
                </button>
              </div>
            </div>
            <div class="border-2 border-gray-500 p-4 mt-4">
              <p class="text-md my-2 text-white">
                Start Spot calibration
              </p>
              <RobotStateCard />
              <div>
                <button
                  type="button"
                  class="uppercase text-md w-full py-2 my-2 px-4 bg-gray-200 text-gray-800
        hover:bg-gray-800 hover:bg-gray-100 hover:text-white"
                  @click="()=>startCalibration()"
                >
                  Start Calibration
                </button>
              </div>
            </div>
          </StepContentContainer>
        </ProgressContainerElement>
      </ProgressContainer>
    </div>
  </div>
</template>

<script>
import { defineComponent } from '@vue/composition-api'
import { computed, ref } from '@nuxtjs/composition-api'
import { signMessage } from '~/plugins/robonomics'
import { useWallet } from '~/store/wallet'
import { useRobot } from '~/store/robot'
import { moveCamera, getAuthToken, zoom } from '~/plugins/camera'
import { calibrateSpot } from '~/plugins/robot'
export default defineComponent({
  setup () {
    const wallet = useWallet()
    const robot = useRobot()
    const zoomAbsolute = ref('173')
    const progressElementStatuses = computed(() => {
      const stagesStatus = {
        connectWallet: (wallet.walletConnectionStatus === 'connected'),
        cameraControl: true
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

    const signToken = async () => {
      console.log(wallet.selectedAccount.account.address)
      const token = await getAuthToken(wallet.selectedAccount.account.address)
      const signedMessage = await signMessage(token)
      console.log(token)
      console.log(signedMessage)
      robot.robotToken = token
      robot.signedRobotToken = signedMessage
    }

    const moveCommand = async (velocity) => {
      await moveCamera(wallet.selectedAccount.account.address, robot.signedRobotToken, velocity)
    }

    const startCalibration = async () => {
      await calibrateSpot(wallet.selectedAccount.account.address, robot.signedRobotToken)
    }
    const zoomCommand = async () => {
      console.log('zoom command')
      await zoom(wallet.selectedAccount.account.address, robot.signedRobotToken, parseInt(zoomAbsolute.value))
    }

    return { wallet, robot, progressElementStatuses, zoomAbsolute, signToken, moveCommand, zoomCommand, startCalibration }
  }
})
</script>
