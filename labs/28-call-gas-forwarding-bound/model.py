"""EIP-150 zero-value allocation arithmetic, not EVM execution."""
def forwarded(available,requested):
    for n in (available,requested):
        if type(n) is not int or n<0: raise ValueError("gas")
    return min(requested,available-available//64)
def execute(available,required,child_ok=True,vulnerable=False):
    delivered=forwarded(available,required)
    if (available if vulnerable else delivered)<required:
        raise ValueError("underfunded")
    if not child_ok: raise ValueError("child failure")
    return delivered
