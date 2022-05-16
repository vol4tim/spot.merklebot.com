<template>
  <main class="bg-gray-100 dark:bg-gray-800 h-screen overflow-hidden relative">
    <div class="flex items-start justify-between">
      <div class="h-screen hidden lg:block shadow-lg relative w-80">
        <div class="bg-white h-full dark:bg-gray-700">
          <div class="flex items-center justify-start pt-6 ml-8">
            <p class="font-bold dark:text-white text-xl">
              Merklebot
            </p>
          </div>
          <nav class="mt-6">
            <div>
              <a
                class="w-full text-gray-800 dark:text-white flex items-center pl-6 p-2 my-2 transition-colors duration-200 justify-start border-l-4 border-purple-500"
                href="#"
              >
                <span class="text-left">
                  <svg
                    width="20"
                    height="20"
                    fill="currentColor"
                    viewBox="0 0 1792 1792"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M1472 992v480q0 26-19 45t-45 19h-384v-384h-256v384h-384q-26 0-45-19t-19-45v-480q0-1 .5-3t.5-3l575-474 575 474q1 2 1 6zm223-69l-62 74q-8 9-21 11h-3q-13 0-21-7l-692-577-692 577q-12 8-24 7-13-2-21-11l-62-74q-8-10-7-23.5t11-21.5l719-599q32-26 76-26t76 26l244 204v-195q0-14 9-23t23-9h192q14 0 23 9t9 23v408l219 182q10 8 11 21.5t-7 23.5z"
                    />
                  </svg>
                </span>
                <span class="mx-2 text-sm font-normal">
                  Home
                </span>
              </a>
              <a
                class="w-full text-gray-400 flex items-center pl-6 p-2 my-2 transition-colors duration-200 justify-start hover:text-gray-800 border-l-4 border-transparent"
                href="#"
              >
                <span class="text-left">
                  <svg
                    width="20"
                    height="20"
                    fill="currentColor"
                    viewBox="0 0 1792 1792"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M1728 608v704q0 92-66 158t-158 66h-1216q-92 0-158-66t-66-158v-960q0-92 66-158t158-66h320q92 0 158 66t66 158v32h672q92 0 158 66t66 158z"
                    />
                  </svg>
                </span>
                <span class="mx-4 text-sm font-normal">
                  Records
                </span>
              </a>
            </div>
          </nav>
        </div>
      </div>
      <div class="flex flex-col w-full md:space-y-4">
        <header class="w-full h-16 z-40 flex items-center justify-between">
          <div class="block lg:hidden ml-6">
            <button class="flex p-2 items-center rounded-full bg-white shadow text-gray-500 text-md">
              <svg
                width="20"
                height="20"
                class="text-gray-400"
                fill="currentColor"
                viewBox="0 0 1792 1792"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M1664 1344v128q0 26-19 45t-45 19h-1408q-26 0-45-19t-19-45v-128q0-26 19-45t45-19h1408q26 0 45 19t19 45zm0-512v128q0 26-19 45t-45 19h-1408q-26 0-45-19t-19-45v-128q0-26 19-45t45-19h1408q26 0 45 19t19 45zm0-512v128q0 26-19 45t-45 19h-1408q-26 0-45-19t-19-45v-128q0-26 19-45t45-19h1408q26 0 45 19t19 45z"
                />
              </svg>
            </button>
          </div>
          <div class="relative z-20 flex flex-col justify-end h-full px-3 md:w-full">
            <AccountChooser />
          </div>
        </header>
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
            </CardContainer>

            <CardContainer title="Drawing panel">
              <DrawingPanel :canvas-id="'canvas-one'" />
            </CardContainer>

            <CardContainer title="Robonomics handlers">
              <ControlPanel />
            </CardContainer>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
export default {
  name: 'IndexPage'
}
</script>
