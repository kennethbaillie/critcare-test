
# Step 1: Set up Google Sheets as a Database
Create a Google Sheet to act as your database.
Label the first row with columns like FileName, DownloadCount.

# Step 2: Create a Google Apps Script to Increment the Counter
Open your Google Sheet.
Click on Extensions > Apps Script.
Replace the code in the script editor with something like this:
javascript
Copy code
// This is the ID of the spreadsheet where you're tracking downloads.
var SPREADSHEET_ID = 'your_spreadsheet_id_here';

function doGet(e) {
  var fileName = e.parameter.file;
  if (fileName) {
    incrementDownloadCount(fileName);
  }
  return ContentService.createTextOutput("Download logged");
}

function incrementDownloadCount(fileName) {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var sheet = ss.getSheetByName('Sheet1'); // or your sheet's name
  var data = sheet.getDataRange().getValues();
  var fileRow = data.findIndex(row => row[0] === fileName);
  
  if (fileRow !== -1) {
    // Increment the existing count
    sheet.getRange(fileRow + 1, 2).setValue(data[fileRow][1] + 1);
  } else {
    // Add a new file entry if it doesn't exist
    sheet.appendRow([fileName, 1]);
  }
}
Replace 'your_spreadsheet_id_here' with your actual Google Sheet ID.
Save and name your project.
Deploy the script as a web app (Deploy > New deployment > Select type > Web app). Set the access to "Anyone, even anonymous" and deploy.

# Step 3: Modify Your GitHub Pages Site
Use JavaScript to send a request to the Google Apps Script Web App URL whenever a PDF link is clicked.

For every PDF link on your GitHub Pages site, add an onclick event to call a JavaScript function, passing the file name as a parameter. For example:
html
Copy code
<a href="path/to/your/file.pdf" onclick="logDownload('file.pdf')">Download PDF</a>
Add the JavaScript function to your site's HTML (in a <script> tag or an external JS file):
javascript
Copy code
function logDownload(fileName) {
  // URL of your Google Apps Script deployment
  var scriptUrl = 'https://script.google.com/macros/s/your_deployment_id/exec';
  
  fetch(scriptUrl + '?file=' + encodeURIComponent(fileName))
    .then(response => console.log('Download logged for', fileName))
    .catch(error => console.error('Error logging download:', error));
}
Important Note: This method exposes your Google Apps Script URL and relies on client-side JavaScript, which means it might not track downloads from users with JavaScript disabled or from direct access through shared links outside your GitHub Pages site. Additionally, because the script URL is publicly accessible, it could be called directly, potentially leading to inaccurate counts if not secured properly.