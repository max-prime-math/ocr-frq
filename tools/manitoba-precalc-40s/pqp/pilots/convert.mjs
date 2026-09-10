import fs from 'node:fs';
import * as bindings from '/home/max/dev/typr/node_modules/mitex-wasm/mitex_wasm_bg.js';
const { instance } = await WebAssembly.instantiate(
  fs.readFileSync('/home/max/dev/typr/node_modules/mitex-wasm/mitex_wasm_bg.wasm'),
  { './mitex_wasm_bg.js': bindings },
);
bindings.__wbg_set_wasm(instance.exports);
const values = JSON.parse(fs.readFileSync(0, 'utf8'));
process.stdout.write(JSON.stringify(values.map(value => bindings.convert_text(value, new Uint8Array()))));
