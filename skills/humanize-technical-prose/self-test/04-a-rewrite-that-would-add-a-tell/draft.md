# Choosing a consistency model

The order service maintains strong consistency for writes, reflecting the team's commitment to
correctness. Reads from the replica can lag the primary by up to two seconds.

Experts argue that eventual consistency is rarely worth its cost for payments.

Use the primary for any read that decides whether to charge a card.
