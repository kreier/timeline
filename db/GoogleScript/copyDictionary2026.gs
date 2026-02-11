function copyDictionary2026() {
  const ui = SpreadsheetApp.getUi();

  const targetSS = SpreadsheetApp.getActive();
  const targetSheet = targetSS.getSheetByName(TAB_NAME);

  if (!targetSheet) {
    ui.alert(`Target sheet "${TAB_NAME}" not found.`);
    return;
  }

  const referenceSS = SpreadsheetApp.openById(REFERENCE_SPREADSHEET_ID);
  const referenceSheet = referenceSS.getSheetByName(TAB_NAME);

  if (!referenceSheet) {
    ui.alert(`Reference sheet "${TAB_NAME}" not found.`);
    return;
  }

  // --- A1:A573 ---
  const colA = referenceSheet.getRange('A1:A573').getValues();
  targetSheet
    .getRange(1, 1, colA.length, colA[0].length)
    .setValues(colA);

  // --- C1:E573 ---
  const colCtoE = referenceSheet.getRange('C1:E573').getValues();
  targetSheet
    .getRange(1, 3, colCtoE.length, colCtoE[0].length)
    .setValues(colCtoE);

  SpreadsheetApp.getActive().toast('Dictionary copied from reference → 2026 ✅', 'Success', 3);
}
