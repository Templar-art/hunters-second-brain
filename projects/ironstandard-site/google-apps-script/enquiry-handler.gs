/**
 * Iron Standard - enquiry handler.
 *
 * Deployed as a Google Apps Script Web App bound to a Google Sheet the
 * client owns. contact.html POSTs here through a hidden iframe, because
 * Apps Script Web Apps do not return CORS headers for fetch().
 *
 * The strategy requires that member, trainer, partnership and general
 * enquiries reach different people. ROUTES below does that. Fill in the
 * addresses at deployment; anything left blank falls back to OWNER.
 *
 * NOTE ON A BUG IN THE PREVIOUS BUILD
 * The earlier waitlist handler notified via
 *   Session.getActiveUser().getEmail()
 * which returns an empty string for anonymous submitters under the
 * "Execute as: Me / Anyone" deployment this project uses. The result was
 * a silent failure: the visitor saw success, nobody was ever emailed.
 * This version never calls getActiveUser(). It uses an explicit constant
 * and falls back to getEffectiveUser(), which does resolve when the
 * script executes as its owner.
 */

/* ------------------------------------------------------------------ */
/* Configuration. Set these once, at deployment.                       */
/* ------------------------------------------------------------------ */

// Leave as '' to fall back to the script owner's address.
var OWNER = '';

var ROUTES = {
  membership:    '',
  coaching:      '',
  trainer:       '',
  physiotherapy: '',
  partnership:   '',
  media:         '',
  general:       ''
};

var TAB_NAME = 'Enquiries';

var HEADER = [
  'Timestamp', 'Type', 'Name', 'Email', 'Detail', 'Message', 'Routed to'
];

/* ------------------------------------------------------------------ */

function doPost(e) {
  try {
    var p = (e && e.parameter) ? e.parameter : {};

    // Honeypot. A real visitor never fills this hidden field; a bot that
    // fills every input does. Accept the request so the bot sees success,
    // but never write a row.
    if (p.website) {
      return jsonResponse({ ok: true });
    }

    var type = String(p.enquiryType || 'general').toLowerCase();
    if (!ROUTES.hasOwnProperty(type)) {
      type = 'general';
    }

    var recipient = resolveRecipient(type);
    var timestamp = new Date();

    appendRow([
      timestamp,
      type,
      p.name || '',
      p.email || '',
      p.extra || '',
      p.message || '',
      recipient
    ]);

    notify(recipient, type, p, timestamp);

    return jsonResponse({ ok: true });
  } catch (err) {
    // Log rather than throw, so a notification failure never costs us the
    // row that was already written.
    console.error('Enquiry handler failed: ' + err);
    return jsonResponse({ ok: false });
  }
}

function doGet() {
  return jsonResponse({ ok: true, service: 'Iron Standard enquiry handler' });
}

function resolveRecipient(type) {
  var target = ROUTES[type];
  if (target) return target;
  if (OWNER) return OWNER;
  // Resolves to the script owner under "Execute as: Me". Unlike
  // getActiveUser(), this does not return empty for anonymous submitters.
  return Session.getEffectiveUser().getEmail();
}

function appendRow(row) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var tab = ss.getSheetByName(TAB_NAME);
  if (!tab) {
    tab = ss.insertSheet(TAB_NAME);
    tab.appendRow(HEADER);
    tab.setFrozenRows(1);
  }
  tab.appendRow(row);
}

function notify(recipient, type, p, timestamp) {
  if (!recipient) return;

  var lines = [
    'Type: ' + type,
    'Name: ' + (p.name || ''),
    'Email: ' + (p.email || '')
  ];
  if (p.extra) lines.push('Detail: ' + p.extra);
  if (p.message) lines.push('', 'Message:', p.message);
  lines.push('', 'Received: ' + timestamp);

  MailApp.sendEmail({
    to: recipient,
    subject: 'Iron Standard: new ' + type + ' enquiry',
    body: lines.join('\n'),
    replyTo: p.email || undefined,
    name: 'Iron Standard website'
  });
}

function jsonResponse(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Run once from the Apps Script editor after deploying. Writes a test row
 * and sends a test notification, so the routing is proven before launch
 * rather than discovered broken afterwards.
 */
function testHandler() {
  var result = doPost({
    parameter: {
      enquiryType: 'coaching',
      name: 'Test submission',
      email: 'test@example.com',
      extra: 'Checking the routing',
      message: 'Delete this row.'
    }
  });
  console.log(result.getContent());
  console.log('Resolved recipient: ' + resolveRecipient('coaching'));
}
