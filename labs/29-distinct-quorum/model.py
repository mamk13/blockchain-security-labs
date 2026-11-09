"""Educational quorum aggregation; attestations are trusted fixtures, not signatures."""
def accepted(members, threshold, attestations, digest, *, vulnerable=False):
    if type(threshold) is not int or not 1 <= threshold <= len(members):
        raise ValueError("unreachable threshold")
    seen = set()
    count = 0
    for signer, signed_digest, valid in attestations:
        if signer not in members or signed_digest != digest or valid is not True:
            return False
        if not vulnerable and signer in seen:
            return False
        seen.add(signer)
        count += 1
    return count >= threshold
