# Solution — Payment liveness and failure isolation

The batch restores all payments after Eve rejects, so Alice and Bob make no progress. Independent claims isolate that failure. Eve's claim remains funded until a later successful claim. Explain why this is a liveness guarantee for other willing recipients, not a guarantee of universal eventual payment.

The corrected path is intentionally narrow. Read the README assumptions before translating the invariant to another execution environment. A green local suite is evidence for these traces, not a security certification.
