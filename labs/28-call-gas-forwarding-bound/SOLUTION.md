# Solution

The cap is available - floor(available/64). At 6400 only 6300 is forwarded; 6501 first permits 6400. Guard the delivered amount, not the pre-cap value. Successful child return is still a separate check.
