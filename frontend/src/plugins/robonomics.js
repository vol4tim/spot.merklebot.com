import { Robonomics, AccountManager } from "robonomics-interface";
import keyring from "@polkadot/ui-keyring";

let robonomics;
let accountsManager;

export const getInstance = async () => {
  if (robonomics) return robonomics;
  robonomics = new Robonomics({
    endpoint: "wss://kusama.rpc.robonomics.network/",
  });
  return robonomics;
};

export const getAccountsManager = async () => {
  if (accountsManager) return accountsManager;
  robonomics.setAccountManager(new AccountManager(keyring));
  accountsManager = robonomics.accountManager;
  return accountsManager;
};

export const connectWallet = async () => {
  const accountManager = await getAccountsManager();
  await accountManager.initPlugin(accountManager.keyring);
};

export const getAccounts = async () => {
  return getAccountsManager().getAccounts();
};

export const setActiveAccount = async (address) => {
  await getAccountsManager().selectAccountByAddress(address);
};

export const makeLaunchTx = (robotAddress, status) => {
  return getInstance().launch.send(robotAddress, status);
};

export const signAndSendWithActiveAccount = async (tx) => {
  return getAccountsManager().signAndSend(tx);
};
