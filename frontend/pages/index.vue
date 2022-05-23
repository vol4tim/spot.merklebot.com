<template>
  <main class="bg-gray-100 dark:bg-gray-800 h-screen overflow-hidden relative">
    <div class="flex items-start justify-between">
      <SidePanel active="Home" />
      <div class="flex flex-col w-full md:space-y-4">
        <HeaderPanel />
        <div class="overflow-auto h-screen pb-24 px-4 md:px-6">
          <h1 class="text-4xl font-semibold text-gray-800 dark:text-white my-2">
            MerkleBot Spot SDK Education
          </h1>
          <h2 class="text-md text-gray-400 my-2">
            Become a certified Boston Dynamics Spot developer at <a
              href="https://spot-sdk.education/"
              rel="noopener noreferrer"
            >https://spot-sdk.education/</a>
          </h2>
          <p>
            Here you can control Boston Dynamics Spot like a student at MerkleBot Spot SDK Basics course.
            <ol>
              <li>1. Compose and send a program to Spot with authorization for your Polkadot account,</li>
              <li>2. Watch the robot executes your program,</li>
              <li>3. Verify your session on Robonomics blockchain and IPFS.</li>
            </ol>
          </p>

          <div v-if="interactionMode==='drawing'" class="grid grid-cols-3 grid-rows-1 md:grid-cols-3 lg:grid-cols-3 gap-4 my-4">
            <CardContainer title="Camera" class="col-span-2">
              <CameraFrame />

              <CardContainer title="Launch data">
                <ControlPanel ref="controlPanel" />
              </CardContainer>
            </CardContainer>

            <CardContainer title="Drawing panel">
              <DrawingPanel :canvas-id="'canvas-one'" @drawing_sent="drawingSent" />
            </CardContainer>

            <CardContainer title="Code example" class="col-span-3">
              <CodeSample />
            </CardContainer>
          </div>
          <div v-if="interactionMode==='movement'" class="grid grid-cols-3 grid-rows-1 md:grid-cols-3 lg:grid-cols-3 gap-4 my-4">
            <CardContainer title="Camera" class="col-span-2">
              <CameraFrame />
            </CardContainer>

            <CardContainer title="Launch data">
              <ControlPanel ref="controlPanel" />
              <button
                type="button"
                class="py-2 px-4 mt-4 bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500 focus:ring-offset-indigo-200 text-white w-full transition ease-in duration-200 text-center text-base font-semibold shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2  rounded-lg "
                @click="()=>drawingSent(()=>{})"
              >
                Send Command
              </button>
            </CardContainer>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
export default {
  name: 'MainPage',
  data: () => {
    return {
      interactionMode: 'drawing'
    }
  },
  mounted () {
    this.updateInteractionMode()
  },
  methods: {
    async drawingSent (sendCommand) {
      await this.$refs.controlPanel.launchCps()
      sendCommand()
    },
    updateInteractionMode () {
      fetch('https://api.merklebot.com/strelka/interaction_mode').then(response => response.json()).then((data) => {
        this.interactionMode = data.interaction_mode
      })
    }
  }
}
</script>
