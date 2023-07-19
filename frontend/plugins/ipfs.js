
import { onMounted, ref } from '@nuxtjs/composition-api'

export function decodeMsg (msg) {
  let json = {}
  try {
    json = JSON.parse(Buffer.from(msg).toString('utf8'))
  } catch (e) {
    throw new Error(e)
  }
  const data = { ...json }
  return data
}

export function encodeMsg (msg) {
  return Buffer.from(JSON.stringify(msg))
}

function loadScript (src) {
  return new Promise(function (resolve, reject) {
    const script = document.createElement('script')
    script.src = src
    script.onload = resolve
    script.onerror = reject
    document.body.appendChild(script)
  })
}

let node

async function create (config) {
  if (node) {
    return node
  }
  node = await window.Ipfs.create(config)
  const info = await node.id()
  console.log('ipfs id ' + info.id)
  return node
}

export function getIpfs () {
  return node
}

export async function init () {
  await loadScript('https://cdn.jsdelivr.net/npm/ipfs@0.61.0/index.min.js')
  const ipfs = create({
    repo: 'ipfs/robonomics/5',
    config: {
      Addresses: {
        Swarm: [
          '/dns4/1.webrtcstar.aira.life/tcp/443/wss/p2p-webrtc-star/',
          '/dns4/2.webrtcstar.aira.life/tcp/443/wss/p2p-webrtc-star/',
          '/dns4/3.webrtcstar.aira.life/tcp/443/wss/p2p-webrtc-star/'
        ]
      },
      Bootstrap: [
        '/dns4/1.pubsub.aira.life/tcp/443/wss/ipfs/QmdfQmbmXt6sqjZyowxPUsmvBsgSGQjm4VXrV7WGy62dv8',
        '/dns4/2.pubsub.aira.life/tcp/443/wss/ipfs/QmPTFt7GJ2MfDuVYwJJTULr6EnsQtGVp8ahYn9NSyoxmd9',
        '/dns4/3.pubsub.aira.life/tcp/443/wss/ipfs/QmWZSKTEQQ985mnNzMqhGCrwQ1aTA6sxVsorsycQz9cQrw'
      ]
    }
  })
  return ipfs
}

export function useIpfs () {
  const ipfs = ref()

  onMounted(() => {
    init().then((r) => {
      ipfs.value = r
    })
  })

  return {
    ipfs
  }
}
