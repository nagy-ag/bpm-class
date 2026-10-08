// BPA nap03: Extensions > Apps Script, a dedicated course spreadsheet.
// The user privately sets CMC_PRO_API_KEY in Project Settings > Script properties.
// Never put its value in source code, a URL, a cell, or a log.
function arfolyamFrissites(e) {
  const API_KEY = PropertiesService.getScriptProperties().getProperty('CMC_PRO_API_KEY');
  const IDS = ['1', '1027', '5426']; // Mini-feladat: add '5426' here.
  if (!API_KEY || !API_KEY.trim()) {
    throw new Error('A CMC_PRO_API_KEY Script property értékét előbb privát módon állítsd be.');
  }
  const url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    + '?id=' + IDS.join(',') + '&convert=EUR';
  let response;
  try {
    response = UrlFetchApp.fetch(url, {
      headers: {'X-CMC_PRO_API_KEY': API_KEY.trim(), Accept: 'application/json'},
      muteHttpExceptions: true,
      followRedirects: false
    });
  } catch (_) {
    throw new Error('A CMC-kérés nem sikerült; ellenőrizd a kapcsolatot és a hozzáférést.');
  }
  let result;
  try { result = JSON.parse(response.getContentText()); }
  catch (_) { throw new Error('Nem JSON-válasz érkezett.'); }
  if (response.getResponseCode() !== 200 || !result.status || result.status.error_code !== 0) {
    throw new Error('CMC-hiba. HTTP: ' + response.getResponseCode());
  }
  const now = new Date();
  const rows = [['Kripto', 'Ár (EUR)', 'Frissítve']];
  IDS.forEach(id => {
    const coin = result.data && result.data[id];
    const price = coin && coin.quote && coin.quote.EUR && coin.quote.EUR.price;
    if (!coin || typeof coin.name !== 'string' || typeof price !== 'number'
        || !Number.isFinite(price) || price <= 0) {
      throw new Error('Hiányzó vagy hibás ár. CMC-azonosító: ' + id);
    }
    rows.push([coin.name, price, now]);
  });
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) throw new Error('A kódot a táblázathoz kötött Apps Script projektben futtasd.');
  const sheet = ss.getSheetByName('ARFOLYAMOK') || ss.insertSheet('ARFOLYAMOK');
  sheet.getRange('A:C').clearContent();
  sheet.getRange(1, 1, rows.length, 3).setValues(rows);
  sheet.getRange(1, 1, 1, 3).setFontWeight('bold');
  sheet.getRange(2, 2, IDS.length, 1).setNumberFormat('0.00');
  sheet.getRange(2, 3, IDS.length, 1).setNumberFormat('yyyy-mm-dd hh:mm:ss');
  sheet.autoResizeColumns(1, 3);
  SpreadsheetApp.flush();
  console.log(JSON.stringify({
    outcome: 'quotes_written', ids: IDS, rows: IDS.length,
    fetched_at: now.toISOString(), provider_timestamp: result.status.timestamp,
    execution: e && e.triggerUid ? 'time_driven' : 'manual'
  }));
}

