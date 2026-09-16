/**
 * Iron Standard — form submission handler.
 *
 * Deployed as a Google Apps Script Web App, bound to the Google Sheet
 * Anthony owns. Both the waitlist form (waitlist.html) and the contact
 * form (contact.html) POST here; the hidden `form` input tells this
 * script which Sheet tab a submission belongs to, so waitlist sign-ups
 * and contact enquiries never mix in the same count.
 *
 * See README.md in this folder for the one-time deployment steps —
 * those steps happen inside Anthony's own Google account and can't be
 * scripted from outside it.
 */
function doPost(e) {
  var params = e.parameter;

  // Honeypot: a real visitor never fills this hidden field. A bot that
  // blindly fills every input on the page does. Silently accept the
  // request (no error shown to the bot) but never write a row for it.
  if (params.website) {
    return jsonResponse({ ok: true });
  }

  var isContact = params.form === 'contact';
  var tabName = isContact ? 'Contact' : 'Waitlist';
  var sheet = SpreadsheetApp.getActiveSpreadsheet();
  var tab = sheet.getSheetByName(tabName);
  if (!tab) {
    tab = sheet.insertSheet(tabName);
    var header = isContact
      ? ['Timestamp', 'Name', 'Email', 'Message']
      : ['Timestamp', 'Name', 'Email'];
    tab.appendRow(header);
  }

  var timestamp = new Date();
  var row = isContact
    ? [timestamp, params.name, params.email, params.message]
    : [timestamp, params.name, params.email];
  tab.appendRow(row);

  var subject = isContact
    ? 'Iron Standard: new contact enquiry'
    : 'Iron Standard: new waitlist sign-up';
  var bodyLines = ['Name: ' + params.name, 'Email: ' + params.email];
  if (isContact) bodyLines.push('Message: ' + params.message);
  bodyLines.push('', 'Logged: ' + timestamp);
  MailApp.sendEmail(Session.getActiveUser().getEmail(), subject, bodyLines.join('\n'));

  return jsonResponse({ ok: true });
}

function jsonResponse(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
