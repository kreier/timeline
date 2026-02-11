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
