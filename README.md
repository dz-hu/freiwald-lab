# Freiwald Lab website

The website of the Laboratory of Neural Systems (Freiwald Lab) at The Rockefeller University.
It is built with [Jekyll](https://jekyllrb.com) and hosted on GitHub Pages.

**You don't need to know HTML to update it.** Almost everything lives in a few text files.
Edit a file, commit it, and the live site updates within a minute or two.

## What to edit

| I want to… | Edit this file |
|---|---|
| Add, change or remove a lab member | `_data/people.yml` |
| Add a member's photo | Put a square photo (about 600×600 px) in `assets/img/people/`, then set `photo:` in `_data/people.yml` |
| Post a news item | Add a new file in `_news/` (see below) |
| Hide a wrong paper, mark a paper as "Selected", or add a PDF/code link | `_data/publications_manual.yml` |
| Add a paper that isn't on PubMed | `extra:` section of `_data/publications_manual.yml` |
| Change the research descriptions | `_data/research.yml` |
| Add gallery photos | Put images in `assets/img/gallery/`, list them in `_data/gallery.yml` |
| Change the contact email, address or menu | `_config.yml` |
| Change colors or fonts | top of `assets/css/main.css` |

Every data file has instructions in comments (`#` lines) at the top.

### Publications are automatic

Every Monday, a GitHub Action downloads the PI's papers from PubMed into
`_data/publications_auto.json`. **Don't edit that file.** Your changes would be overwritten.
Use `_data/publications_manual.yml` instead. To update the list right away, go to the
repository on GitHub → **Actions** → **Update publications** → **Run workflow**.

### Adding a news item

Create a file in `_news/` named `YYYY-MM-DD-short-name.md`, for example
`_news/2026-12-01-new-postdoc.md`:

```markdown
---
date: 2026-12-01
---
A warm welcome to Jane Doe, who joins the lab as a postdoc!
```

The five newest items appear on the home page automatically. `_news/_template.md.txt` is a template you can copy.

## Editing on GitHub (no installation)

1. Open the file on github.com and click the ✏️ pencil icon.
2. Make your change and click **Commit changes**.
3. Wait 1–2 minutes and reload the website.

To upload a photo: open the folder (e.g. `assets/img/people/`) → **Add file** → **Upload files**.

YAML is sensitive to indentation. Copy an existing entry and keep the same spacing.
If the site doesn't update, check the **Actions** tab for a red ❌. It usually means a
YAML indentation mistake.

## Previewing locally (optional)

Requires Ruby 3.3 (GitHub Pages doesn't support Ruby 4 yet). On macOS:

```bash
brew install ruby@3.3
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"
bundle config set --local path vendor/bundle
bundle install
bundle exec jekyll serve
```

Then open <http://localhost:4000>. To refresh publications locally, run `python3 scripts/fetch_pubmed.py`.

## Project layout

```
_config.yml                 site settings, menu, contact info
_data/                      people, research, publications, gallery
_news/                      one file per news item
_layouts/, _includes/       page templates (rarely need changes)
assets/css/main.css         styles
assets/img/                 images (people/, research/, gallery/)
scripts/fetch_pubmed.py     PubMed download script
.github/workflows/          weekly publication update
```
