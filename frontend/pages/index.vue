<template>
  <main class="bg-gray-100 dark:bg-gray-800 h-screen overflow-hidden relative">
    <div class="flex items-start justify-between">
      <SidePanel active="Home" />
      <div class="flex flex-col w-full md:space-y-4">
        <HeaderPanel />
        <div class="overflow-auto h-screen pb-24 px-4 md:px-6">
          <h1 class="text-4xl font-semibold text-gray-800 dark:text-white">
            Spot demo
          </h1>
          <h2 class="text-md text-gray-400">
            Here&#x27;s spot controlling demo.
          </h2>
          <div class="grid grid-cols-3 grid-rows-1 md:grid-cols-3 lg:grid-cols-3 gap-4 my-4">
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
        </div>
      </div>
    </div>
  </main>
</template>

<script>
export default {
  name: 'MainPage',
  methods: {
    drawingSent () {
      this.$refs.controlPanel.launchCps()
    }
  }
}
</script>
