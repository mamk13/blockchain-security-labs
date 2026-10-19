# Exercise — Atomic upgrade migration

Use a migration that keeps total100 but changes balances from Alice70/Bob30 to Alice0/Bob100. Is total conservation sufficient? Next fail after a partial write and retry the correct migration. Finally mutate an external list and explain why the local snapshot cannot restore it.

Write the failing assertion first. Record the runtime, command and actual result. Explain which assumption your test depends on and which omitted behavior needs an integration test.

