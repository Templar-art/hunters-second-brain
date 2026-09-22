# Enquiry handler: deployment

The contact form posts to a Google Apps Script Web App bound to a Google Sheet.
These steps happen inside the client's own Google account and cannot be scripted
from outside it.

## One-time setup

1. Create a Google Sheet in the account that should own the enquiry data. Name it
   something like `Iron Standard enquiries`.
2. In that Sheet: **Extensions → Apps Script**.
3. Delete the placeholder `Code.gs` and paste in `enquiry-handler.gs` from this
   folder. Save.
4. Fill in the configuration at the top of the script:
   - `OWNER` — the address that receives anything unrouted.
   - `ROUTES` — one address per enquiry type. Leave a type blank to send it to
     `OWNER`. This is what keeps trainer and partnership leads out of the member
     inbox, which the strategy asks for.
5. **Deploy → New deployment → Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
   - Deploy, authorise, then copy the **Web app URL**.
6. Run `testHandler` once from the editor. Confirm a row lands in the Sheet and
   the notification email arrives. Do not skip this step: it is the check the
   previous build did not have.

## Wiring the site

Open `contact.html` and replace the placeholder on the form:

```html
<form ... data-endpoint="PASTE_WEB_APP_URL_HERE">
```

Until a real URL is in place the form stays deliberately inert and tells the
visitor so, rather than appearing to send and silently discarding the enquiry.

## Why a hidden iframe and not fetch()

Apps Script Web Apps do not return CORS headers, so a `fetch()` POST from the
site's own origin is blocked. The form targets a hidden iframe instead, which is
not subject to the same restriction. This is the same pattern the earlier build
used and it is known to work.

## Bug this version fixes

The previous handler notified via `Session.getActiveUser().getEmail()`. Under the
"Execute as: Me / Anyone" deployment above, that returns an empty string for
anonymous submitters, so `MailApp.sendEmail` was called with no recipient and the
notification silently never fired while the visitor still saw success. This
version never calls `getActiveUser()`. It uses an explicit `OWNER` constant and
falls back to `getEffectiveUser()`, which resolves correctly when the script runs
as its owner.

## Data handling

Only the fields the form collects are stored: enquiry type, name, email, the
conditional detail field and the message. Nothing is added to a mailing list.
The privacy page must be finalised with legal review before launch.
