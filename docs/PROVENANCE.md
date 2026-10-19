# Provenance

## October 19, 2026 — Labs 15–18

Four new synthetic Python exercises were developed on remote main `7aec1fadfcee43538de8dfa599e568138e1a2d97`: transient frame lifetime, code/storage context, packed-layout compatibility, and atomic upgrade migration. References: EIP-1153, EIP-7, EIP-1967, Solidity documentation and OpenZeppelin upgrade guidance. No upstream implementation was copied. Existing owner edits and Labs 01–14 source/tests were retained. Documentation separates the specification, tested model, negative controls and exclusions; this is not a claim of incident discovery, sole human authorship, a production patch or bytecode validation.

Maintainer: Mohammad Khezer.

The first lab comes from the September 2026 Blockchain Security Review educational artifact. It uses original synthetic examples, not copied deployed protocol code. The initial repository publication retains the artifact's three Python source files and adds navigation, exercises and a dated validation record.

Claims about incident discoveries, independent exploit reproduction and production validation require their own evidence; maintenance of this repository alone does not establish them.

Preserve source attribution and license notices when adding third-party material. Commit history records actual changes; test records distinguish local runs from hosted CI. The project has not yet adopted an open-source license.

Lab 03 was prepared October 5, 2026 and prepared for publication October 6. It is an original synthetic model inspired by the public CWA-2026-006 advisory. No Wasmer, wasmvm or wasmd code was copied, and no native escape was reproduced.

Lab 04 was prepared October 5, 2026 and published October 7, 2026. It is an original synthetic deployment-policy model based on the public CWA-2026-006 advisory. No Wasmer, wasmvm or wasmd source was copied. The lab is not a production attestation service, updater, upstream patch or exploit replay.

Lab 05 was prepared October 8, 2026. It is an original synthetic oracle-consumer model based on Chainlink's public EVM Data Feeds documentation. No Chainlink contract or deployed protocol source was copied. The lab is not a production feed adapter, oracle recommendation, incident reconstruction or deployed patch.

Lab 06 was prepared October 8, 2026. It is an original synthetic share-accounting model based on EIP-4626 and OpenZeppelin's public ERC-4626 guide. No OpenZeppelin contract or deployed vault source was copied. The lab is not an ERC-4626 implementation, audited vault, deployed patch or exploit replay.

Labs 07 and 08 were developed October 12, 2026 as original synthetic Python models. Sources: ERC-1271 and OpenZeppelin's public SignatureChecker/Initializable documentation. No protocol or library code was copied. Lab 07 tests current authorization policy; Lab 08 tests initialized-instance registration. Neither is an EVM implementation, audited production component or exploit replay.



## October15,2026 — Labs09–14

Added six distinct educational exercises on epochs, authorization domains, callback ordering, payment liveness, received-amount credit and Merkle claim binding. Built on remote main a67ab76a84461239e16279a02de658b48eed117c; existing owner changes and source/test files preserved. Sources are references, not installed dependencies or copied implementations. Individual READMEs distinguish trusted fixtures, negative controls, guarantees and excluded behavior. No incident reconstruction, production patch, sole-authorship claim or live financial testing is asserted.
