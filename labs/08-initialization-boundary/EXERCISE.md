# Exercise — successful call, wrong state

Run the suite on CPython 3.12.14. In a disposable copy, remove AtomicFactory's initialization postcondition. Predict the behavior of NoOpImplementation and WrongOwnerImplementation before running their tests.

Then add a test with two proxies using one implementation: Alice owns the first, Bob owns the second, and the implementation's own storage stays uninitialized and locked against direct initialization.

Explain it yourself: why does a one-time initializer fail to identify the rightful first caller? What must an authenticated factory bind besides the intended owner? Why does checking a nonempty code flag not make arbitrary implementation code trustworthy?

