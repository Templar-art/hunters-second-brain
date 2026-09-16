# Iron Standard — form backend (Google Apps Script)

`waitlist-handler.gs` in this folder receives both the waitlist form
(`waitlist.html`) and the contact form (`contact.html`) submissions and
writes each into its own tab of a Google Sheet, plus emails a
notification for every new row.

This has to be deployed from inside Anthony's own Google account — it
can't be scripted from outside it. One-time setup:

1. Create (or open) the Google Sheet that will hold submissions.
2. In that Sheet, **Extensions > Apps Script**.
3. Delete the default empty `Code.gs` content, and paste in the contents
   of `waitlist-handler.gs` from this folder.
4. **Deploy > New deployment > Web app.**
   - Execute as: **Me**.
   - Who has access: **Anyone**. (This has to be public so the form on
     the live site can reach it. It is not a secret — Apps Script Web
     Apps are meant to work this way, the same way the URL you're
     about to copy is not an API key.)
5. Click Deploy, authorize the script when Google prompts for it, and
   copy the **Web app URL** it gives you.
6. In the site's `waitlist.html` and `contact.html`, replace every
   occurrence of `REPLACE_WITH_APPS_SCRIPT_WEB_APP_URL` with that real
   URL (one `<form action="...">` per file).
7. Submit a test entry through the live waitlist form and confirm a row
   appears in the Sheet and a notification email arrives.

**If you ever need to change the script:** edit it in the Apps Script
editor, then **Deploy > Manage deployments > edit (pencil icon) > New
version > Deploy**. Editing the code alone does not update the live
Web App URL's behavior until you deploy a new version.

**Two tabs, one Sheet:** submissions land on a "Waitlist" tab or a
"Contact" tab depending on which form sent them, so a contact enquiry
never inflates the waitlist count. Both tabs are created automatically
on first submission — nothing to set up by hand.
