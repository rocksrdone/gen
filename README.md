# Genealogy widgets for Grist

Custom Grist widgets for the **Family History Research** doc (Stash team site).

| Widget | Bind it to | URL (after GitHub Pages is on) |
|---|---|---|
| Person profile | `People` | `https://rocksrdone.github.io/gen/person/` |
| Family tree | `People` | `https://rocksrdone.github.io/gen/tree/` |
| DNA match helper | `DNA_Matches` | `https://rocksrdone.github.io/gen/dna/` |
| Sources workbench | `Sources` | `https://rocksrdone.github.io/gen/sources/` |
| Record entry | `Sources` | `https://rocksrdone.github.io/gen/entry/` |
| Spanish record helper | any table (no access needed) | `https://rocksrdone.github.io/gen/glossary/` |

## Adding a widget in Grist

1. On a page, **Add New → Add widget to page → Custom**, and choose the table above.
2. In the creator panel, choose **Custom URL** and paste the widget URL.
3. Set **Access level** to **Full document access**. Every widget reads several tables, and the DNA helper also adds rows.

## What each widget does

- **Person profile**: a full page for the selected person. It shows vitals, the birth-year check, family links you can click to move around, an evidence timeline, a chart of the birth year each stated age implies, name variants, conclusions, open questions, dead ends, Ancestry sync items, DNA matches and family stories. A search box jumps to anyone.
- **Family tree**: an hourglass tree with up to 3 generations above and below, plus siblings and spouses. Lines are dashed for relationships that aren't proven, and card borders show each person's status. Click anyone to centre the tree on them.
- **DNA match helper**: a quick-entry form for AncestryDNA matches with a live relationship guess. For the selected match it charts where the shared cM falls on the Shared cM Project ranges. It also has a cluster summary, a list of all matches sorted by cM, and shared-match entry.

- **Sources workbench**: browse and filter sources (by type, extraction status, or no image yet). Open the record or image, drag, paste or choose images to upload straight into the source, set the extraction status (which stamps the date), edit the transcription, and add evidence rows for any person without leaving the page. New sources get the next S-code, and tracking parameters are stripped from pasted links.

- **Record entry**: paste an Ancestry or FamilySearch link (film, image and record IDs are pulled out, tracking junk removed), pick the record type and get a role-based form (baptism/birth: child, parents, grandparents; marriage: couple and both sets of parents; death; census household). Names are matched to people already in the doc, including alternate spellings (b/v, s/z, g/j). One Save creates the source, new people, evidence rows (age, origin, residence, occupation, marital status, "finado"), name spellings and relationships, adding the source as proof to relationships that already exist.

- **Spanish record helper**: a searchable glossary of about 220 Spanish and Latin words, phrases, abbreviations and old spellings from Mexican civil and parish records (Spanish or English search). It also has a "decode a passage" box that highlights known words and turns number words into digits, and a number reader ("mil novecientos treinta" = 1930). Edit `glossary/terms.js` to add words.

## Tables and columns the widgets expect

People, Relationships, Evidence, Sources, Names, Places, Searches, Ancestry_Sync, Conclusions, ToDo, Stories, DNA_Matches, DNA_Clusters, DNA_Kits, DNA_Shared. These use the column names created when the doc was set up. If you rename a column, update the widget code too.

## Local testing

`python3 test/make_fixture.py && python3 test/run.py` renders each widget with sample data and a mock Grist API (Playwright), then saves screenshots in `test/`.
