function importCsvToHL() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getActiveSheet();
  const folderId = "folder_for_csv_files"; // Replace with your folder ID

  // Get language code from sheet name
  const langCode = sheet.getName().trim().toLowerCase();

  // Build filename like dictionary_en.csv
  const csvFileName = `dictionary_${langCode}.csv`;

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
