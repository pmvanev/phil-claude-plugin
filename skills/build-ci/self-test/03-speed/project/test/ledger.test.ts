import { expect, test } from "vitest";
import { balance } from "../src/ledger";

test("balances the entries", () => {
  expect(balance([10, -4])).toBe(6);
});
