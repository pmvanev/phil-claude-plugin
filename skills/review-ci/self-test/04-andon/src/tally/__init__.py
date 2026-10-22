def total(ledgers):
    return sum(float(line.split()[-1]) for ledger in ledgers for line in ledger.splitlines() if line.strip())
