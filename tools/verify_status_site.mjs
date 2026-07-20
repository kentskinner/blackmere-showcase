import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const html = readFileSync('index.html', 'utf8');
const references = [...html.matchAll(/(?:href|src)="([^"]+)"/g)]
  .map((match) => match[1])
  .filter((value) => !value.startsWith('#') && !value.startsWith('http'));
const missing = references.filter((value) => !existsSync(resolve(value)));
const status = JSON.parse(readFileSync('status.json', 'utf8'));

if (missing.length > 0) {
  throw new Error(`Missing local references: ${missing.join(', ')}`);
}

if (
  typeof status.stage !== 'number' ||
  typeof status.deterministicTests !== 'number' ||
  status.browserJourneys?.passed !== status.browserJourneys?.total
) {
  throw new Error('status.json does not contain a complete passing verification snapshot');
}

console.log(
  `Status site verified: ${references.length} local references, stage ${status.stage}, ` +
    `${status.deterministicTests} tests, ${status.browserJourneys.passed}/${status.browserJourneys.total} browser journeys.`,
);
