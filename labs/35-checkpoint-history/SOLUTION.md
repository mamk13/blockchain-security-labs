# Solution and design trade-off

Answers are 0,20,20,90. A tick can have multiple writes before it closes, so serving it as immutable history is premature. bisect_right yields the position after all keys <=query; read its predecessor. A trusted clock prevents insertion into closed history and prevents user-supplied far-future keys from pinning the sequence. This does not establish consensus finality; it only preserves the model's time-order contract.

