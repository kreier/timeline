// ID of dictionary_reference Google Sheet
const REFERENCE_SPREADSHEET_ID = 'folder_for_csv_files';
const TAB_NAME = '2026';

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Timeline Translation Tools')
    .addItem('Import Reference English', 'copyDictionary2026')
    .addItem("Order Deprecated", "orderDeprecated")
    .addItem("Import CSV", "importCsvToHL")
    .addItem("Export CSV", "exportCsvFromHL")
    .addToUi();
}

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

function importCsvToHL() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getActiveSheet();
  const folderId = "folder_for_csv_files";

  const spreadsheetName = SpreadsheetApp.getActiveSpreadsheet().getName();
  const csvFileName = spreadsheetName + ".csv";

  const folder = DriveApp.getFolderById(folderId);
  const files = folder.getFilesByName(csvFileName);

  if (!files.hasNext()) {
    SpreadsheetApp.getUi().alert("CSV file not found: " + csvFileName);
    return;
  }

  const file = files.next();
  const csvContent = file.getBlob().getDataAsString();
  let data = Utilities.parseCsv(csvContent);

  // Optional: remove header row if detected
  if (data.length && data[0].length > 0 && isNaN(data[0][0])) {
    data.shift();
  }

  // Normalize cells: whitespace-only → empty
  data = data.map(row =>
    row.map(cell =>
      typeof cell === "string" && cell.trim() === "" ? "" : cell
    )
  );

  // Limit rows to H2:L572
  const maxRows = 571;
  data = data.slice(0, maxRows);

  // Ensure exactly 5 columns (H–L)
  data = data.map(row => {
    const r = row.slice(0, 5);
    while (r.length < 5) r.push("");
    return r;
  });

  sheet.getRange(2, 8, data.length, 5).setValues(data);

  SpreadsheetApp.getUi().alert("CSV imported successfully.");
}

function exportCsvFromHL() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const folderId = "folder_for_csv_files";

  const spreadsheetName = SpreadsheetApp.getActiveSpreadsheet().getName();
  const csvFileName = spreadsheetName + ".csv";

  // Read H2:M572 (6 columns)
  const startRow = 2;
  const numRows = 571;
  const data = sheet.getRange(startRow, 8, numRows, 6).getValues();

  const header = ["key", "text", "english", "notes", "tag", "checked"];

  const escapeCsv = value => {
    const str = value.toString();
    return str.includes(",") || str.includes('"') || str.includes("\n")
      ? `"${str.replace(/"/g, '""')}"`
      : str;
  };

  const rows = data.map(row =>
    row.map(cell => {
      if (cell === "" || cell === null) return " ";
      if (cell === true) return "True";
      if (cell === false) return "False";
      if (cell instanceof Date) {
        return Utilities.formatDate(
          cell,
          SpreadsheetApp.getActive().getSpreadsheetTimeZone(),
          "yyyy-MM-dd"
        );
      }
      return cell;
    }).map(escapeCsv).join(",")
  );

  // Force CRLF line endings to match PANDAS
  const csvContent =
    ([header.join(",")].concat(rows))
      .join("\r\n") + "\r\n";

  const folder = DriveApp.getFolderById(folderId);
  const files = folder.getFilesByName(csvFileName);

  if (files.hasNext()) {
    files.next().setContent(csvContent);
  } else {
    folder.createFile(csvFileName, csvContent, MimeType.CSV);
  }

  SpreadsheetApp.getUi().alert("CSV exported successfully (LF, Python booleans).");
}
