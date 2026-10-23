import { expect, test } from "vitest";
import { total } from "../src/tally.js";
import { ledger } from "./support/ledger.js";

test("totals the amount column, skipping the header", () => {
  expect(total(ledger(["rent,1200", "coffee,4.50"]))).toBe(1204.5);
});
