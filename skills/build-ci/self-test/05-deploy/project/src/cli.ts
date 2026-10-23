#!/usr/bin/env node
import { readFileSync } from "node:fs";
import { total } from "./tally.js";

const lines = readFileSync(process.argv[2], "utf8").trim().split("\n");
console.log(total(lines).toFixed(2));
