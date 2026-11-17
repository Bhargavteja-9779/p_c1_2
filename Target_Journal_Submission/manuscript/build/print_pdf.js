
const { chromium } = require('playwright');
(async () => {
  const [html, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + html, { waitUntil: 'load' });
  await page.pdf({ path: out, format: 'A4', printBackground: true, displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: "<div style='font-size:8pt;width:100%;text-align:center'><span class='pageNumber'></span></div>",
    margin: { top: '20mm', bottom: '20mm', left: '18mm', right: '18mm' } });
  await browser.close();
})();
