# Sick Calf Exam app

Livestock Veterinary Resources, LLC · built with Claude.

**Source of truth:** this repo, at [`health_records/sick_calf/index.html`](../health_records/sick_calf/index.html).
It is the file the website links to, so it must be edited here. (The *output* the app
produces is what flows into LVRRecords — the UI does not live there.)

**Public URL:** <https://livestockveterinaryresources.com/health_records/sick_calf>
(reached from the site under Calf Care → Sick Calf Exam, and from the printed QR code).

A single self-contained web page a client fills out beside a sick calf, then copies the
summary and sends it to the clinic however they like. No server, no database, no login —
it runs entirely in the phone browser. The one file is portable and can be hosted on any
static web host unchanged.

## How it's served

The file lives at `health_records/sick_calf/index.html`. `health_records` is listed under
`resources:` in `_quarto.yml`, so Quarto copies the folder verbatim into `_site/` on
`quarto render`, and it deploys with the rest of the site to `gh-pages`. Serving it at the
path `/health_records/sick_calf` is why the folder is named this way.

## Fields, in order

- **Client name** (text; the account name, not necessarily the person filling it out)
- **Calf ID or name** (text)
- **Rectal temperature, °F** (number; a gentle warning appears below 95 or above 108)
- **Manure / fecal consistency**: Watery, Pudding, Normal, Dry, Other (Other opens a describe box)
- **Attitude**: Normal, Depressed, Can't stand, Can't hold head up
- **Flank**: Normal, Mildly / Moderately / Severely sunk, Mild / Moderate / Severe full (bloat)
- **Eyes**: Normal, Mildly / Moderately / Severely sunk
- **Umbilicus (navel)**: Normal, Mild, Moderate, Severe
- **Other notes** (free text)
- **Appetite** (last section): Today and Yesterday, each with feedings at 7 a.m., 1 p.m.,
  7 p.m., 1 a.m. Each feeding records pints (1–6), Milk or Electrolytes, and Sucked or Tubed.
  All feedings are optional.

## Summary behaviour

"Create exam summary" builds a plain-text report: calf ID, client, date and time, each finding
(unanswered items show as "not recorded"), the filled-in feedings, then computed daily totals of
milk and electrolytes in pints per day. Pints entered without a milk/electrolytes selection are
totalled as "type not marked" rather than guessed into a category. Notes come last. Totals exist
only in the summary; there is no totals input on the form.

## Sending

- **Copy as text**: copies the plain-text summary to the clipboard so the client can paste it
  wherever they want — a text message, email, or notes. The summary is kept as plain text
  deliberately so it can later be parsed into a database on the LVRRecords side.
- **Start a new exam**: reloads a blank form.

Nothing sends silently; the client always pastes and sends in their own app, so replies go back
to them.

(An earlier version also offered send-as-picture and email buttons; those were removed to keep
the flow simple. The `CLINIC_PHONE` / `CLINIC_EMAIL` constants at the top of the script are now
vestigial and can be removed on the next edit.)

## Updating it

Edit `health_records/sick_calf/index.html` in this repo, then `quarto render` and publish
(`quarto publish gh-pages`) as with the rest of the site. Because it's a plain resource file,
the render just copies it — no page metadata to worry about.

## QR code

A print-ready QR code that opens the public URL (with the LVR logo in the centre, high error
correction) lives in [`qr/`](../qr/): `sick_calf_qr.png` (standalone) and
`sick_calf_qr_card.pdf` (barn-card / hutch-sign). Regenerate with `qr/make_qr.py` after
changing the logo or URL.
