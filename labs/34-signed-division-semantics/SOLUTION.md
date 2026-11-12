# Solution and design trade-off

Opposite-sign operands with a nonzero remainder expose the difference. Compute magnitude with integer arithmetic, apply the quotient sign, then derive r=a-q*b. Converting a/b through a float loses exactness near int256 bounds. Floor subtracts one from a nonintegral negative truncating quotient. Neither rounding rule is automatically economically correct; compare the chosen policy with the deployed runtime. Python can represent abs(MIN), unlike an int256 positive intermediate; this is an oracle, not a Solidity port.

