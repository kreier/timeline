// ID of dictionary_reference Google Sheet
const REFERENCE_SPREADSHEET_ID = 'file_id_of_dictionary_reference_sheet'; // Replace with your sheet ID

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Timeline Translation Tools')
    .addItem('Import Reference English', 'copyDictionary2026')
    .addItem("Order Deprecated", "orderDeprecated")
    .addItem("Import CSV", "importCsvToHL")
    .addItem("Export CSV", "exportCsvFromHL")
    .addToUi();
}
