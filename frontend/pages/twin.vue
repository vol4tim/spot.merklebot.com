<template>
  <main class="bg-gray-800 overflow-hidden relative">
    <div class="flex items-start justify-between">
      <!--      <SidePanel active="Records" />-->
      <div class="flex flex-col w-full md:space-y-4">
        <div class="overflow-auto pb-24 px-4 md:px-6">
          <div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4 my-4">
              <CardContainer title="Digital twin">
                <!--                <URDFFrame urdf-url="/urdf/spot.urdf.xacro" ros-url="ws://10.200.0.3:9494" />-->
                <!--                <URDFFrame urdf-url="/urdf/spot.urdf.xacro" ros-url="ws://localhost:8000/robots/1/realtime_ws" />-->
                <RosbagPlayer urdf-url="/urdf/spot.urdf.xacro" ros-url="ws://localhost:8000/robots/1/realtime_ws" />
              </CardContainer>

              <!--              <CardContainer v-if="launchData" title="Digital twin">-->
              <!--                <RosbagPlayer :rosbag-url="`${makeIpfsFolderLink(traceInfo)}/state.bag`" />-->
              <!--              </CardContainer>-->
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>

</script>
