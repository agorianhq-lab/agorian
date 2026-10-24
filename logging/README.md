# Agorian class logging

Each device gets a random id. Students type a name on first visit, which is recorded with their answers. No logins.

1. Create a Google Sheet called "Agorian log".
2. Extensions > Apps Script. Paste `Code.gs`. Save.
3. Deploy > New deployment > Web app. Execute as Me. Access: Anyone. Deploy. Copy the `/exec` URL.
4. In `src/index.html` set `LOG_ENDPOINT` to that URL.
5. In the Sheet: File > Share > Publish to web. Choose the `events` sheet, CSV. Copy the link.
6. In `src/index.html` set `TEACHER_CSV` to that link.
7. `python3 build.py`, commit, push. The teacher view at `#teacher` now reads the whole class.

The `summarise()` function in the script builds a "summary" tab on demand (Run > summarise).
