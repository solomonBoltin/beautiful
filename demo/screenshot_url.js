const chromium = require('@sparticuz/chromium').default || require('@sparticuz/chromium');
const puppeteer = require('puppeteer-core');
(async () => {
  const browser = await puppeteer.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800, deviceScaleFactor: 1 });
  await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36');
  const [url, out] = process.argv.slice(2);
  try { await page.goto(url, { waitUntil: 'networkidle2', timeout: 25000 }); } catch (e) { console.error('warn:', e.message); }
  await new Promise(r => setTimeout(r, 800));
  await page.screenshot({ path: out });
  console.log('ok', url);
  await browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
