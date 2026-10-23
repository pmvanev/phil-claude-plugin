import { createServer } from "node:http";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { total } from "./tally.js";

// Each environment sets TALLY_LEDGER_DIR; nothing about an environment is built into the image.
const dir = process.env.TALLY_LEDGER_DIR ?? "/var/lib/tally";

createServer((req, res) => {
  const name = (req.url ?? "/").slice(1).replace(/[^a-z0-9-]/gi, "");
  const lines = readFileSync(join(dir, `${name}.csv`), "utf8").trim().split("\n");
  res.end(`${total(lines).toFixed(2)}\n`);
}).listen(8080);
