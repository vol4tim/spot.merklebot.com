import {
  Robonomics,
  AccountManager as RobonomicsAccountManager,
} from "robonomics-interface";
import AccountManager from "robonomics-interface/dist/accountManagerUi";
import keyring from "@polkadot/ui-keyring";

let robonomics;

export const getInstance = async () => {
  if (robonomics) return robonomics;
  robonomics = new Robonomics({
    endpoint: "wss://kusama.rpc.robonomics.network/",
  });
  robonomics.setAccountManager(new RobonomicsAccountManager(keyring));
  await robonomics.run();
  await AccountManager.initPlugin(robonomics.accountManager.keyring);
  return robonomics;
};

export const getAddresses = async () => {
  const robonomics = await getInstance();
  const accounts = await robonomics.accountManager.getAccounts();
  return accounts.map((account) => account.address);
};
