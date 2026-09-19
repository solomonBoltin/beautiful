const chromium = require('@sparticuz/chromium').default || require('@sparticuz/chromium');
const puppeteer = require('puppeteer-core');
(async () => {
  const browser = await puppeteer.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });
  const [file, out, script] = process.argv.slice(2);
  await page.goto('file://' + file, { waitUntil: 'networkidle0' }).catch(()=>{});
  if (script) await page.evaluate(script);
  await new Promise(r => setTimeout(r, 300));
  await page.screenshot({ path: out });
  await browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
