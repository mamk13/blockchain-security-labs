# Exercise — Packed layout compatibility

Store balance100 and debt3 in two uint128 fields. Swap their declaration order without changing slot count, then decode the unchanged word. Add a field after both and contrast the result. Explain why an implementation metadata slot does not validate this application schema.

Write the failing assertion first. Record the runtime, command and actual result. Explain which assumption your test depends on and which omitted behavior needs an integration test.

