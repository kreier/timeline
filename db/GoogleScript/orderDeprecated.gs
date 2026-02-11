function orderDeprecated() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

  const startRow = 541;
  const numRows = 572 - 541 + 1;

  // Reference range A–E
  const reference = sheet
    .getRange(startRow, 1, numRows, 5)
    .getValues();

  // Target range H–L
  const target = sheet
    .getRange(startRow, 8, numRows, 5)
    .getValues();

  // Build lookup map from column H
  const targetMap = {};
  target.forEach(row => {
    const key = row[0]; // column H
    if (key !== "") {
      targetMap[key] = row;
    }
  });

  // Reorder target based on column A
  const reordered = reference.map(refRow => {
    const key = refRow[0]; // column A
    return targetMap[key] || ["", "", "", "", ""];
  });

  // Write reordered data back to H–L
  sheet
    .getRange(startRow, 8, reordered.length, 5)
    .setValues(reordered);

  SpreadsheetApp.getUi().alert("Deprecated entries reordered successfully.");
}
