# Solution

A one-time guard only prevents the second initialization. In the vulnerable sequence, Eve succeeds first; Alice is rejected correctly by the wrong security policy.

Removing the postcondition registers no-op or wrong-owner candidates. Checking both the initialized flag and expected owner catches these modeled failures. A real deployment must verify every required initialized field and trusted implementation identity, not just copy this pair of checks.

For the two-proxy exercise, create one locked Implementation, deploy_initialized('a', i, 'alice') and deploy_initialized('b', i, 'bob'), assert distinct Storage objects and owners, and assert i.storage.initialized is false. A direct call with direct=True must reject. This models separate storage; it does not execute delegatecall.

Trade-off: publish only a fully configured instance, accepting deployment failure when setup cannot complete. A deliberate two-step deployment needs a separate authorization boundary that the vulnerable factory lacks. Initialization failure must not strand a registered, claimable instance.

