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
