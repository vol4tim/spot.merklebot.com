<template>
  <video
    id="video"
    autoplay="true"
    playsinline="true"
    muted="true"
  />
</template>

<script>
export default {
  name: 'VideoContainer',
  data () {
    return {
      pc: null
    }
  },
  mounted () {
    this.initPc()
    this.negotiate()
  },
  methods: {
    negotiate () {
      //  creates a new RTCRtpTransceiver `video` and adds it to the
      // set of transceivers associated with the RTCPeerConnection
      this.pc.addTransceiver('video', {
        direction: 'recvonly'
      })
      // create and return  SDP offer for the purpose
      // of starting a new WebRTC connection to a remote peer
      return this.pc
        .createOffer()
        .then((offer) => {
          return this.pc.setLocalDescription(offer)
        })
        .then(() => {
          // wait for ICE gathering to complete
          return new Promise((resolve) => {
            if (this.pc.iceGatheringState === 'complete') {
              resolve()
            } else {
              const checkState = () => {
                if (this.pc.iceGatheringState === 'complete') {
                  // remove `icegatheringstatechange` event listener
                  this.pc.removeEventListener('icegatheringstatechange', checkState)
                  resolve()
                }
              }

              // add `icegatheringstatechange` event listener
              this.pc.addEventListener('icegatheringstatechange', checkState)
            }
          })
        })
        .then(() => {
          // build and return json offer.
          const offer = this.pc.localDescription
          return fetch(process.env.VIDEOSERVER_URL + '/offer', {
            body: JSON.stringify({
              sdp: offer.sdp,
              type: offer.type
            }),
            headers: {
              'Content-Type': 'application/json'
            },
            method: 'POST'
          })
        })
        .then((response) => {
          // return response
          return response.json()
        })
        .then((answer) => {
          // return session description as the
          // remote peer's current answer.
          return this.pc.setRemoteDescription(answer)
        })
        .catch((e) => {
          // catch any errors.
          alert(e)
        })
    },
    initPc () {
      const config = {
        sdpSemantics: 'unified-plan'
      }
      config.iceServers = [
        {
          urls: ['stun:stun.l.google.com:19302']
        }
      ]
      this.pc = new RTCPeerConnection(config)
      this.pc.addEventListener('track', function (evt) {
        if (evt.track.kind === 'video') {
          document.getElementById('video').srcObject = evt.streams[0]
        }
      })
    }
  }
}

</script>

<style scoped>

</style>
