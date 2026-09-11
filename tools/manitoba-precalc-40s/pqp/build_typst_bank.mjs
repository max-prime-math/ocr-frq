// Build in a separate directory, validate with TestGen, and record input hashes.
// Usage: node build_typst_bank.mjs BANK JOBS OUTPUT TESTGEN
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const [bank, jobsFile, output, testgen] = process.argv.slice(2);
const require = createRequire(import.meta.url);
const {importRepoEntriesToAppData,exportAppDataToRepoEntries,hashRepoDataContent} = require(path.join(testgen,'src/git/repoDataModel.ts'));
const manifest=JSON.parse(fs.readFileSync(path.join(bank,'manifest.json'),'utf8'));
const entries=[...manifest.files.map(({path:p})=>({path:p,kind:'file',content:p.startsWith('images/')?new Uint8Array(fs.readFileSync(path.join(bank,p))):fs.readFileSync(path.join(bank,p),'utf8')})),{path:'manifest.json',kind:'file',content:fs.readFileSync(path.join(bank,'manifest.json'),'utf8')}];
const app=importRepoEntriesToAppData(entries).appData;
const baseline=Object.fromEntries(entries.map(e=>[e.path,hashRepoDataContent(e.content)]));
const byId=new Map(app.questions.map(q=>[q.id,q]));
const jobs=JSON.parse(fs.readFileSync(jobsFile,'utf8'));
for(const job of jobs) {
  if(typeof job.typst!=='string')throw Error('Missing conversion: '+job.id+' '+job.field);
  if(/\\[A-Za-z]{2,}/.test(job.typst))throw Error('LaTeX remains: '+job.id+' '+job.field);
  const q=byId.get(job.id); if(!q)throw Error('Unknown question: '+job.id);
  if(job.field.startsWith('choice:'))q.choices[job.field.split(':')[1]]=job.typst;
  else q[job.field]=job.typst;
  q.updatedAt=Date.now();
}
for(const q of app.questions) {
  const text=[q.body,q.solution,...Object.values(q.choices??{})].join('\n');
  const names=[...text.matchAll(/#image\("\/imgs\/([^"/]+)"/g)].map(m=>m[1]);
  q.images=[...new Set(names)].sort();
}
const generated=exportAppDataToRepoEntries(app);
const readme=generated.find(e=>e.path==='README.md');
readme.content='# Manitoba Pre-Calculus 40S Provincial Exams\n\n967 questions from 21 exam sittings, with native Typst question bodies, choices, and solutions.\n\nSource: Manitoba Education student booklets and marking guides, available at https://www.edu.gov.mb.ca/k12/assess/archives/ . Original wording and diagrams belong to their publisher.\n\nAll converted fields have been compile-checked. This is an OCR-derived bank: mathematical accuracy and complex layouts still need editorial review. Six targeted editorial repairs are documented in the OCR project.\n\nUse this folder in TestGen Local folder storage, or the private GitHub repository. OCR files, conversion scripts, and review PDFs live in the separate ocr-frq project.\n';
const m=generated.find(e=>e.path==='manifest.json'); const data=JSON.parse(m.content);
const rm=data.files.find(e=>e.path==='README.md');rm.size=Buffer.byteLength(readme.content);rm.hash=hashRepoDataContent(readme.content);
m.content=JSON.stringify(data,null,2);
const checked=importRepoEntriesToAppData(generated);
const roundtrip=exportAppDataToRepoEntries(checked.appData);
const sig=es=>es.filter(e=>!['manifest.json','README.md'].includes(e.path)).sort((a,b)=>a.path.localeCompare(b.path)).map(e=>e.path+':'+hashRepoDataContent(e.content)).join('|');
if(sig(generated)!==sig(roundtrip))throw Error('Local-folder round trip changed bank data');
if(fs.existsSync(output))throw Error('Output already exists: '+output);
for(const e of generated) {const p=path.join(output,e.path);fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,e.content);}
fs.writeFileSync(output+'-baseline.json',JSON.stringify(baseline,null,2));
console.log(JSON.stringify({questions:checked.appData.questions.length,images:checked.appData.images.length,fields:jobs.length,import:'passed',roundtrip:'passed',output}));
