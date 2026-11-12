# Solution and design trade-off

The wrapped product is 0 modulo 2**256, so the negative control returns 0. Checked multiplication rejects the wide intermediate; the specification returns 2**200. Let M=2**256-1 and use x=y=M-1, d=M-2: the exact ratio is M+1/(M-2), so floor is M and ceiling overflows. Dividing x first loses its remainder; 7*5/3 floors to 11 while (7//3)*5 yields 10. Production use requires a vetted wide-intermediate implementation and runtime tests, not pasting this Python oracle.

