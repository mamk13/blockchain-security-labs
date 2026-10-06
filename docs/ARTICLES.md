# Article index

## A Smart Contract Sandbox Is Only as Strong as Its Compiler Boundary

- [Published Medium article](https://medium.com/@mamk13/a-smart-contract-sandbox-is-only-as-strong-as-its-compiler-boundary-e48ed3c01e61), supplied by the author October 5, 2026.
- Disclosure review of CWA-2026-006, publicly disclosed September 28, 2026.
- Companion: [Lab 03](../labs/03-sandbox-boundary/README.md), a synthetic capability-boundary model.
- This model does not reproduce the Wasmer defect or replace the upstream patches.

## The Upgrade Path Is Part of Your Security Boundary

- Preliminary review of the September 22, 2026 Neutron incident, drafted September 28.
- Medium publication pending; no URL invented.
- Companion: [Lab 02](../labs/02-upgrade-intent/README.md), an independent educational model of action binding and delays.
- Payload substitution is not established as the Neutron root cause. No chain-specific patch or exploit replay is claimed.

## One Deposit, Two Valid Requests: The Backing Invariant an Amount Check Cannot Prove

- Type: educational review, originally prepared September 21, 2026.
- Companion: [Lab 01](../labs/01-backing-and-replay/README.md).
- [Read the Medium article](https://mamk13.medium.com/one-deposit-two-valid-requests-the-backing-invariant-an-amount-check-cannot-prove-917230f79e10). Publication reported by the author on September 28, 2026.
- Scope: fee arithmetic and source-event consumption; no historical exploit replay.

## Symbiosis Bitcoin Bridge: When a Valid Signature Carries an Invalid Amount

- [Published Medium article](https://mamk13.medium.com/symbiosis-bitcoin-bridge-when-a-valid-signature-carries-an-invalid-amount-b84f3b0dd01b).
- Related reading only. Lab 01 is not the protocol's source or an upstream patch and does not assert replay as the incident's root cause.
- Do not treat the article's incident claims as independently verified by these tests.

## Technical reference

[EIP-712](https://eips.ethereum.org/EIPS/eip-712) specifies typed-data signing and leaves replay protection to applications. This Python lab does not implement EIP-712.
