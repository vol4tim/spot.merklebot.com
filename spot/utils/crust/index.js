import { ApiPromise, WsProvider, Keyring } from "@polkadot/api";
import { typesBundleForPolkadot } from "@crustio/type-definitions";

const args = process.argv.slice(2);
const crustChainEndpoint = "wss://rpc.crust.network";
// const crustChainEndpoint = "wss://rpc-rocky.crust.network";

const api = new ApiPromise({
  provider: new WsProvider(crustChainEndpoint),
  typesBundle: typesBundleForPolkadot,
});

async function placeStorageOrder(mnemonic, cid, size) {
  await api.isReadyOrError;

  // 1. Construct place-storage-order tx
  const tips = 0;
  const memo = "";
  const tx = api.tx.market.placeStorageOrder(cid, size, tips, memo);

  // 2. Load seeds(account)
  const kr = new Keyring({ type: "sr25519" });
  const krp = kr.addFromUri(mnemonic);

  // 3. Send transaction
  const txHash = await tx.signAndSend(krp)

  return `${txHash}`
}

async function getOrderState(cid) {
  await api.isReadyOrError;
  return await api.query.market.filesV2(cid);
}

placeStorageOrder(process.env.MNEMONIC, args[0], args[1]).then((txHash) => {
  console.log(txHash)
  process.exit()
})

// getOrderState(args[0]).then(state => {
//   console.log(state);
//   process.exit();
// })
