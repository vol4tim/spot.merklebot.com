<template>
  <main class="bg-gray-100 dark:bg-gray-800 h-screen overflow-hidden relative">
    <div class="flex items-start justify-between">
      <SidePanel />
      <div class="flex flex-col w-full md:space-y-4">
        <HeaderPanel />
        <div class="overflow-auto h-screen pb-24 px-4 md:px-6">
          <h1 class="text-4xl font-semibold text-gray-800 dark:text-white">
            Spot demo
          </h1>
          <h2 class="text-md text-gray-400">
            Here&#x27;s spot controlling demo.
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4 my-4">
            <CardContainer title="Camera">
              <CameraFrame />

              <CardContainer title="Launch data">
                <ControlPanel />
              </CardContainer>
            </CardContainer>

            <CardContainer title="Drawing panel">
              <DrawingPanel :canvas-id="'canvas-one'" />
            </CardContainer>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
