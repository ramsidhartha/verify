import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

const VerifiTrustModule = buildModule("VerifiTrustModule", (m) => {
  const verifiTrust = m.contract("VerifiTrust");

  return { verifiTrust };
});

export default VerifiTrustModule;