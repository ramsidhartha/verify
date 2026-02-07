import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

const VerifiTrustModule = buildModule("VerifiTrustModule", (m) => {
  // Deploy the contract
  const verifiTrust = m.contract("VerifiTrust");

  // Return the deployed contract instance
  return { verifiTrust };
});

export default VerifiTrustModule;