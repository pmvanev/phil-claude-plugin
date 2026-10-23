export function total(lines: string[]): number {
  return lines
    .slice(1)
    .map((line) => Number(line.split(",")[1]))
    .reduce((sum, amount) => sum + amount, 0);
}
