import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
const require=createRequire(import.meta.url);
const modules=process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
let pw;
try { pw = modules ? require(modules+'/playwright') : require('playwright'); }
catch { throw new Error('Install playwright: npm install playwright && npx playwright install chromium'); }
const root=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const mermaid=process.env.TISE_MERMAID_JS;
if(!mermaid) throw new Error('Set TISE_MERMAID_JS to local mermaid.min.js');
const browser=await pw.chromium.launch({headless:true,executablePath:process.env.TISE_BROWSER_EXE,args:['--no-sandbox']});
const page=await browser.newPage({viewport:{width:1600,height:1200}});
await page.setContent('<html><body style="margin:0;font-family:DejaVu Sans"><div id="out"></div></body></html>');
await page.addScriptTag({path:mermaid});
await page.evaluate(()=>mermaid.initialize({startOnLoad:false,securityLevel:'strict',theme:'base',fontFamily:'DejaVu Sans',themeVariables:{fontFamily:'DejaVu Sans',fontSize:'22px',primaryColor:'#e9f3f5',primaryTextColor:'#183b50',primaryBorderColor:'#007f85',lineColor:'#42616f',secondaryColor:'#fbefdf',tertiaryColor:'#f7fafb'},flowchart:{htmlLabels:false,curve:'linear',padding:20,nodeSpacing:35,rankSpacing:50}}));
const dir=path.join(root,'assets','diagrams');
for(const file of (await fs.readdir(dir)).filter(x=>x.endsWith('.mmd'))){
 await page.evaluate(isSlide=>mermaid.initialize({startOnLoad:false,securityLevel:'strict',theme:'base',fontFamily:'DejaVu Sans',themeVariables:{fontFamily:'DejaVu Sans',fontSize:isSlide?'26px':'22px',primaryColor:'#e9f3f5',primaryTextColor:'#183b50',primaryBorderColor:'#007f85',lineColor:'#42616f',secondaryColor:'#fbefdf',tertiaryColor:'#f7fafb'},flowchart:{htmlLabels:false,curve:'linear',padding:isSlide?14:20,nodeSpacing:isSlide?30:35,rankSpacing:isSlide?36:50}}),file.startsWith('slides-'));
 const source=await fs.readFile(path.join(dir,file),'utf8');
 const svg=await page.evaluate(async s=>(await mermaid.render('tise_'+Math.random().toString(36).slice(2),s)).svg,source);
 await fs.writeFile(path.join(dir,file.replace('.mmd','.svg')),svg);
 console.log(file);
}
await browser.close();
