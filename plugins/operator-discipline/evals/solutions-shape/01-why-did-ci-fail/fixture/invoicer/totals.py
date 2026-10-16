def total_with_vat(net_pence: int, rate: float = 0.2) -> int:
    """Gross amount in pence, rounded half up."""
    return int(net_pence * (1 + rate) + 0.5)
