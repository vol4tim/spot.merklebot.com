<template>
  <div>
    <v-tour name="dappTour" :steps="steps" :callbacks="tourCallbacks" />
  </div>
</template>

<script>
export default {
  name: 'MainTour',
  data () {
    return {
      tourCallbacks: {
        onFinish: this.onFinishCallback,
        onSkip: this.onSkipCallback
      },
      steps: [
        {
          target: '#spot-greeting',
          header: {
            title: '<span class="font-bold text-orange-600">Get Started</span>'
          },
          content: 'This demo will allow you to make real Spot draw anything you want!'
        },
        {
          target: '#camera-frame-container',
          header: {
            title: '<span class="font-bold text-orange-600">Camera</span>'
          },
          content: 'This is realtime video stream of Spot located in our laboratory in San Francisco'
        },
        {
          target: '#anchor-to-1',
          header: {
            title: '<span class="font-bold text-orange-600">Connect your wallet</span>'
          },
          content: "First, you need to connect your PolkadotService wallet to our app <br/><br/> If you don't have it yet, follow <a class='text-orange-600' href='https://polkadot.js.org/extension/' target='_blank'>the link</a> and reload this page after creating new account"
        },
        {
          target: '#anchor-to-2',
          header: {
            title: '<span class="font-bold text-orange-600">Get robot\'s money</span>'
          },
          content: 'To pay a robot for his actions, you need to have XRT cryptocurrency or special ticket <br/><br/> If you don\'t have anything, you can buy it here'
        },
        {
          target: '#drawing-panel-canvas',
          header: {
            title: '<span class="font-bold text-orange-600">Draw your picture</span>'
          },
          content: 'Draw something that you want spot to repeat in this box'
        },
        {
          target: '#drawing-panel-launch',
          header: {
            title: 'Launch action'
          },
          content: 'Choose preferred way to pay a robot\'s work and launch action.<br/><br/> After you sign a transaction to Robonomics blockchain, robot will start executing your command'
        },
        {
          target: '#anchor-to-4',
          header: {
            title: 'See your data'
          },
          content: 'Here you can see data related to robot\'s work'
        }
      ]
    }
  },
  mounted () {
    this.$tours.dappTour.start()
  },
  methods: {
    onFinishCallback () {
      console.log('tour finished')
      this.$emit('finished')
    },
    onSkipCallback () {
      console.log('tour skipped')
      this.$emit('finished')
    }
  }

}
</script>

<style scoped>

</style>
