/**
 * Agorian anonymous answer log. Google Apps Script bound to a Google Sheet.
 *
 * Setup (five minutes, once):
 *  1. Create a new Google Sheet. Name it "Agorian log".
 *  2. Extensions > Apps Script. Delete the sample code, paste this whole file, save.
 *  3. Deploy > New deployment > Type: Web app.
 *       Description: Agorian log
 *       Execute as: Me
 *       Who has access: Anyone
 *     Click Deploy, authorise when asked, copy the Web app URL (ends in /exec).
 *  4. Paste that URL into LOG_ENDPOINT near the top of the site's script, rebuild, publish.
 *  5. In the Sheet: File > Share > Publish to web > sheet "events", format CSV, Publish.
 *     Copy that CSV link into TEACHER_CSV in the site to make the teacher view read the whole class.
 *
 * What is stored: a timestamp, a random per-device session id (no names, no logins),
 * the question id, unit, topic, type, mode, and whether the answer was correct.
 * Nothing identifies a student.
 */

const SHEET = 'events';
const HEAD = ['received', 'sid', 't', 'event', 'mode', 'qid', 'unit', 'topic', 'type', 'correct', 'n', 'c', 'miss', 'right', 'secs'];

function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents || '{}');
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let sh = ss.getSheetByName(SHEET);
    if (!sh) { sh = ss.insertSheet(SHEET); sh.appendRow(HEAD); sh.setFrozenRows(1); }
    const row = [new Date()].concat(HEAD.slice(1).map(k => body[k] === undefined ? '' : body[k]));
    sh.appendRow(row);
    return ContentService.createTextOutput('ok');
  } catch (err) {
    return ContentService.createTextOutput('error ' + err);
  }
}

// Optional: a quick summary tab you can glance at. Run once from the editor, or add a trigger.
function summarise() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sh = ss.getSheetByName(SHEET); if (!sh) return;
  const rows = sh.getDataRange().getValues(); const h = rows.shift();
  const i = Object.fromEntries(h.map((k, n) => [k, n]));
  const byQ = {}, byTopic = {}, sids = new Set();
  rows.forEach(r => {
    if (r[i.event]) return; // skip non-answer events
    sids.add(r[i.sid]);
    const q = r[i.qid], t = r[i.topic], ok = Number(r[i.correct]) === 1;
    byQ[q] = byQ[q] || { topic: t, a: 0, c: 0 }; byQ[q].a++; if (ok) byQ[q].c++;
    byTopic[t] = byTopic[t] || { a: 0, c: 0 }; byTopic[t].a++; if (ok) byTopic[t].c++;
  });
  let out = ss.getSheetByName('summary'); if (!out) out = ss.insertSheet('summary'); out.clear();
  out.appendRow(['Devices seen', sids.size]); out.appendRow([]);
  out.appendRow(['Topic', 'Attempts', 'Correct', 'Accuracy']);
  Object.entries(byTopic).sort((a, b) => a[1].c / a[1].a - b[1].c / b[1].a).forEach(([t, s]) => out.appendRow([t, s.a, s.c, Math.round(100 * s.c / s.a) + '%']));
  out.appendRow([]); out.appendRow(['Question id', 'Topic', 'Attempts', 'Correct', 'Accuracy']);
  Object.entries(byQ).sort((a, b) => a[1].c / a[1].a - b[1].c / b[1].a).forEach(([q, s]) => out.appendRow([q, s.topic, s.a, s.c, Math.round(100 * s.c / s.a) + '%']));
}
