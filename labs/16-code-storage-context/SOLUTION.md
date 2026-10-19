# Solution — Code and storage context

Assert storage on both sides, not only a returned value. The corrected delegate_forwarder retains parent.storage and parent.sender while selecting new code. A normal call changes storage owner to the target and sender to the calling account. Nested delegation must preserve the original owner.

Read the README limits before translating the pattern. Passing these traces is not a general safety proof.

