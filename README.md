# Genealogy widgets for Grist

Custom Grist widgets for the **Family History Research** doc (Stash team site).

| Widget | Bind it to | URL (after GitHub Pages is on) |
|---|---|---|
| Person profile | `People` | `https://rocksrdone.github.io/genealogy-widgets/person/` |
| Family tree | `People` | `https://rocksrdone.github.io/genealogy-widgets/tree/` |
| DNA match helper | `DNA_Matches` | `https://rocksrdone.github.io/genealogy-widgets/dna/` |

## Adding a widget in Grist

1. On a page, **Add New → Add widget to page → Custom**, and choose the table above.
2. In the creator panel, choose **Custom URL** and paste the widget URL.
3. Set **Access level** to **Full document access**. Every widget reads several tables, and the DNA helper also adds rows.

## What each widget does

- **Person profile**: a full page for the selected person. It shows vitals, the birth-year check, family links you can click to move around, an evidence timeline, a chart of the birth year each stated age implies, name variants, conclusions, open questions, dead ends, Ancestry sync items, DNA matches and family stories. A search box jumps to anyone.
- **Family tree**: an hourglass tree with up to 3 generations above and below, plus siblings and spouses. Lines are dashed for relationships that aren't proven, and card borders show each person's status. Click anyone to centre the tree on them.
- **DNA match helper**: a quick-entry form for AncestryDNA matches with a live relationship guess. For the selected match it charts where the shared cM falls on the Shared cM Project ranges. It also has a cluster summary, a list of all matches sorted by cM, and shared-match entry.

## Tables and columns the widgets expect

People, Relationships, Evidence, Sources, Names, Places, Searches, Ancestry_Sync, Conclusions, ToDo, Stories, DNA_Matches, DNA_Clusters, DNA_Kits, DNA_Shared. These use the column names created when the doc was set up. If you rename a column, update the widget code too.

## Local testing

`python3 test/make_fixture.py && python3 test/run.py` renders each widget with sample data and a mock Grist API (Playwright), then saves screenshots in `test/`.
