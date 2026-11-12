# Solution and design trade-off

Use the fixed proposal snapshot for each voter rather than a live balance or now-1 per vote. Snapshot 5 assigns Alice=100/Bob=0 even after current weight moves. Snapshot 8 may instead assign Alice=0/Bob=100; the new proposal can count Bob. The provider must give immutable, correct historical weights in compatible units. Source failure must not consume the voter marker. Fixed snapshots do not by themselves prevent capture before the snapshot, prove correct delegation, or guarantee a good quorum rule.

