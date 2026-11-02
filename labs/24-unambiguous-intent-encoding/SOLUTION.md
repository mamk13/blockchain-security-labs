# Solution and design trade-off

The collision occurs in serialization before hashing. Explicit fixed-width lengths recover the boundary; the decoder rejects ambiguity and trailing data. The exhaustive small-domain test covers1600 pairs and roundtrips each one. Fixed codec version is not application domain separation. A second independent consumer still accepts, so replay remains separate.

A passing model is a reproducible boundary argument, not production certification. Keep the negative control: it proves the suite can distinguish the intended failure.

