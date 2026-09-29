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
      return reply({ ok: true });
    }

    // Never trust the browser. Trim, cap every field at the same limits the
    // form sets, and refuse a request with no usable name or email.
    var name = clean(p.name, 120);
    var email = clean(p.email, 254);
    if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
      return reply({ ok: false, error: 'invalid' });
    }
    p = {
      enquiryType: p.enquiryType,
      name: name,
      email: email,
      extra: clean(p.extra, 200),
      message: clean(p.message, 5000)
    };

    var type = String(p.enquiryType || 'general').toLowerCase();
    if (!ROUTES.hasOwnProperty(type)) {
      type = 'general';
    }

    var recipient = resolveRecipient(type);
    var timestamp = new Date();

    // Serialise writes so two enquiries arriving together cannot collide.
    var lock = LockService.getScriptLock();
    lock.waitLock(10000);
    try {
      appendRow([
        timestamp,
        type,
        cell(p.name),
        cell(p.email),
        cell(p.extra),
        cell(p.message),
        recipient
      ]);
    } finally {
      lock.releaseLock();
    }

    notify(recipient, type, p, timestamp);

    return reply({ ok: true });
  } catch (err) {
    // Log rather than throw, so a notification failure never costs us the
    // row that was already written.
    console.error('Enquiry handler failed: ' + err);
    return reply({ ok: false });
  }
}

function clean(value, max) {
  return String(value || '').trim().slice(0, max);
}

// A value starting with = + - @ is run as a formula by Sheets. A leading
// apostrophe stores it as plain text, so a message like "=IMPORTXML(...)"
// can never execute inside the enquiry sheet.
function cell(value) {
  return /^[=+\-@\t\r]/.test(value) ? "'" + value : value;
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

// The form posts into a hidden iframe, so the page cannot read a JSON body
// (no CORS). Instead answer with a tiny page that tells the parent window
// whether the enquiry was stored. The site listens for this message; without
// it, the only signal is that *something* loaded, which a server error also
// produces.
function reply(obj) {
  var msg = JSON.stringify({ source: 'iron-standard-enquiry', ok: !!obj.ok, error: obj.error || null });
  return HtmlService
    .createHtmlOutput('<script>window.top.postMessage(' + msg + ', "*");</script>')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
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
