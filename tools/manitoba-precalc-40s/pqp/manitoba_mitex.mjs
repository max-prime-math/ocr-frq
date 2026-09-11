// A trapped WASM instance cannot be reused. Both bindings and memory are reset.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const directory = process.env.MITEX_WASM_DIR
  || path.join(os.homedir(), 'dev/typr/node_modules/mitex-wasm');
const bytes = fs.readFileSync(path.join(directory, 'mitex_wasm_bg.wasm'));
let bindings;
let generation = 0;
async function reset() {
  bindings = await import(pathToFileURL(path.join(directory, 'mitex_wasm_bg.js')).href + '?instance=' + generation++);
  const { instance } = await WebAssembly.instantiate(bytes, { './mitex_wasm_bg.js': bindings });
  bindings.__wbg_set_wasm(instance.exports);
}
await reset();
const results = [];
for (const value of JSON.parse(fs.readFileSync(0, 'utf8'))) {
  try {
    results.push({ text: bindings.convert_text(value, new Uint8Array()) });
  } catch (error) {
    results.push({ error: String(error) });
    await reset();
  }
}
process.stdout.write(JSON.stringify(results));
