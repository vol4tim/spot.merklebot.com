<template>
  <div class="flex">
    <div
      class="overflow-x-hidden overflow-y-auto h-screen snap-y snap-mandatory"
    >
      <div
        class="screen flex items-center snap-always snap-center scroll-my-10"
      >
        <div
          class="dark:bg-gray-700 border-2 border-gray-800 dark:border-white mx-6 my-12 px-6 py-8 align-middle"
        >
          <a id="anchor-to-1" href="#1">
            <h3
              id="anchor-to-1"
              class="max-w-md text-xl md:text-2xl font-bold mx-6 dark:text-white text-gray-800"
            >
              1. User Ownership of Data
            </h3>
          </a>
          <p class="text-md my-2 dark:text-white mx-6">
            Identity and access rights are managed using the cryptographic key
            from your Web3 wallet. This way we make sure that you own the data
            generated during your interaction with the robot. And for enterprise
            cases we cryptographically verify the whole chain of custody for
            machine data within and accross organizations.
          </p>
          <div class="flex items-center justify-center">
            <AccountChooser />
            <div v-if="wallet.walletConnectionStatus === 'error'">
              <p class="text-xl my-6 text-center dark:text-white font-bold">
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
          <div />
        </div>
      </div>

      <div
        class="screen flex items-center snap-always snap-center scroll-my-10"
      >
        <div
          class="dark:bg-gray-700 border-2 border-gray-800 dark:border-white mx-6 my-12 px-6 py-8"
        >
          <a id="anchor-to-2" href="#2">
            <h3
              id="2"
              class="max-w-md text-xl md:text-2xl font-bold mx-6 dark:text-white text-gray-800"
            >
              2. Robots Transfer Value
            </h3>
          </a>
          <p class="text-md my-2 dark:text-white mx-6">
            Billing for robot’s work can happen in both US dollars and
            cryptocurrencies - money for robots. While robots today can already
            navigate our complex world, perform inspections and even interact
            with people - they still couldn’t participate in our economy
            directly. From fun demos like this one to data-driven equipment
            leasing: now robots can transact in fully autonomous supply chains.
          </p>

          <PurchaseTicket class="mt-4 mx-6 pr-16 w-full" />
        </div>
      </div>

      <div
        class="screen flex items-center snap-always snap-center scroll-my-10"
      >
        <div
          class="dark:bg-gray-700 border-2 border-gray-800 dark:border-white mx-6 my-12 px-6 py-8"
        >
          <a id="anchor-to-3" href="#3">
            <h3
              id="3"
              class="max-w-md text-xl md:text-2xl font-bold mx-6 dark:text-white text-gray-800"
            >
              3. Secure Access to Machines
            </h3>
          </a>
          <p class="text-md my-2 dark:text-white mx-6">
            Teleoperation session is authorized by the key in your wallet and
            the data can be encrypted with it too. You will now send a
            transaction directly to the robot and it will be recorded in
            Robonomics blockchain within Polkadot ecosystem. This way technical
            command and value transfer are tied together and verified to ensure
            resiliency of large scale cyber-physical systems.
          </p>

          <p class="text-md my-2 dark:text-white mx-6">
            Now you can collaborate with Spot, draw anything in the box and ask
            her to repeat it:
          </p>

          <div class="flex items-center justify-center mt-4">
            <DrawingPanel :canvas-id="'canvas-one'" />
          </div>
        </div>
      </div>

      <div
        class="screen flex items-center snap-always snap-center scroll-my-10"
      >
        <div
          class="dark:bg-gray-700 border-2 border-gray-800 dark:border-white mx-6 my-12 px-6 py-8"
        >
          <a id="anchor-to-4" href="#4">
            <h3
              id="4"
              class="w-full text-xl md:text-2xl font-bold mx-6 dark:text-white text-gray-800"
            >
              4. Decentralized Storage and Reporting
            </h3>
          </a>
          <p class="text-md my-2 dark:text-white mx-6">
            Most secure and affordable way to store large amounts of machine
            data. Large data sets that robots generate are recorded using
            Filecoin Network. It uses cryptographic storage proofs to verify
            data is being stored correctly and securely over time in
            decentralized network of storage providers. All with signifficantly
            lower storage costs compared to traditional clouds.
          </p>
          <p class="text-md my-2 dark:text-white mx-6">
            Here you can see a report from your interaction with Spot:
          </p>
          <ResultingRecordCard />
        </div>
      </div>

      <div
        class="screen flex items-center snap-always snap-center scroll-my-10 mb-32"
      >
        <div
          class="dark:bg-gray-700 border-2 border-gray-800 dark:border-white mx-6 my-12 px-6 py-8"
        >
          <a id="anchor-to-5" href="#5">
            <h3
              id="anchor-to-5"
              class="w-full text-xl md:text-2xl font-bold mx-6 dark:text-white text-gray-800"
            >
              5. Digital Economies Powering Physical World
            </h3>
          </a>
          <p class="text-md my-2 dark:text-white mx-6">
            With the rise of cryptocurrencies adoption new digital market
            flourished and they present a number of opportunities to reduce
            costs, drive additional revenue streams and partnerships.
          </p>
          <div class="flex flex-row mx-8 py-4">
            <div class="basis-1/3 mx-2 px-2 dark:bg-gray-600 relative">
              <h4
                class="max-w-sm text-md md:text-xl font-bold dark:text-white text-gray-800 mt-4"
              >
                DeFi pools and DAOs (costs 📉)
              </h4>
              <p class="text-md my-4 mb-16 dark:text-white">
                Data-driven leasing model unlocks global funding sources for new
                robotics deployments.
              </p>
              <a
                href="https://docs.google.com/presentation/d/1iMaQJuA91D2bHG1LefyikUMNoGKSNqsXwCDAjztJ9xw/edit?usp=sharing"
                target="_blank"
                class="absolute bottom-0 inset-x-0 uppercase py-2 mx-4 my-2 px-4 md:mt-16 bg-transparent dark:text-gray-800 dark:bg-white hover:dark:bg-gray-100 border-2 border-gray-800 text-gray-800 dark:text-white hover:bg-gray-800 hover:text-white text-md text-center"
              >
                Case study
              </a>
            </div>

            <div class="basis-1/3 mx-2 px-2 dark:bg-gray-600 relative">
              <h4
                class="max-w-sm text-md md:text-xl font-bold dark:text-white text-gray-800 mt-4"
              >
                NFT and data markets (revenue 📈)
              </h4>
              <p class="text-md my-4 mb-16 dark:text-white">
                The birth of digital markets present unique opportunities to
                form supporting community around equipment operators.
              </p>

              <a
                href="https://telescope.merklebot.com/#/"
                target="_blank"
                class="absolute bottom-0 inset-x-0 uppercase py-2 mx-4 my-2 px-4 md:mt-16 bg-transparent dark:text-gray-800 dark:bg-white hover:dark:bg-gray-100 border-2 border-gray-800 text-gray-800 dark:text-white hover:bg-gray-800 hover:text-white text-md text-center"
              >
                Check dApp
              </a>
            </div>
            <div class="basis-1/3 mx-2 px-2 dark:bg-gray-600 relative">
              <h4
                class="max-w-sm text-md md:text-xl font-bold dark:text-white text-gray-800 mt-4"
              >
                Plug-and-play integrations (optimization 📊)
              </h4>
              <p class="text-md my-4 mb-16 dark:text-white">
                Open infrastructure and wide hardware support opens endless
                opportunities for data-driven partnerships and collaboration.
              </p>

              <a
                href="https://docs.google.com/presentation/d/1iMaQJuA91D2bHG1LefyikUMNoGKSNqsXwCDAjztJ9xw/edit?usp=sharing"
                target="_blank"
                class="absolute bottom-0 inset-x-0 uppercase py-2 mx-4 my-2 px-4 md:mt-16 bg-transparent dark:text-gray-800 dark:bg-white hover:dark:bg-gray-100 border-2 border-gray-800 text-gray-800 dark:text-white hover:bg-gray-800 hover:text-white text-md text-center"
              >
                Case study
              </a>
            </div>
          </div>
          <p class="dark:text-white mx-6">
            To learn more send us an email to
            <span class="text-orange-600 font-bold">v@merklebot.com</span>.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from '@vue/composition-api'
import { useWallet } from '~/store/wallet'

export default defineComponent({
  setup () {
    const wallet = useWallet()

    return { wallet }
  }
})
</script>
