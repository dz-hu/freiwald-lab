#!/usr/bin/env python3
"""Fetch the lab's publications from PubMed and write _data/publications_auto.json.

Standard library only (runs on GitHub Actions without installing anything).

    python3 scripts/fetch_pubmed.py

Do not edit the generated JSON by hand -- put corrections, extra links,
highlights and exclusions in _data/publications_manual.yml instead.
"""
import difflib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

# "Freiwald W" also matches papers that list him without the middle initial.
QUERY = "Freiwald W[Author]"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
TOOL = "lab-website-publications"
OUT = Path(__file__).resolve().parent.parent / "_data" / "publications_auto.json"
BATCH = 100


def get_json(endpoint, **params):
    params.update(retmode="json", tool=TOOL)
    url = EUTILS + endpoint + "?" + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.load(r)
        except Exception as e:  # network hiccup / rate limit
            if attempt == 3:
                raise
            print(f"retrying after error: {e}", file=sys.stderr)
            time.sleep(2 * (attempt + 1))


def search_pmids():
    res = get_json("esearch.fcgi", db="pubmed", term=QUERY, retmax=1000)
    return res["esearchresult"]["idlist"]


def summarize(pmids):
    out = []
    for i in range(0, len(pmids), BATCH):
        chunk = pmids[i:i + BATCH]
        res = get_json("esummary.fcgi", db="pubmed", id=",".join(chunk))["result"]
        out.extend(res[p] for p in res.get("uids", []))
        time.sleep(0.4)  # stay under NCBI's 3 requests/second limit
    return out


def to_record(s):
    ids = {a["idtype"]: a["value"] for a in s.get("articleids", [])}
    year_match = re.search(r"\d{4}", s.get("sortpubdate") or s.get("pubdate") or "")
    pubtypes = s.get("pubtype", [])
    rec = {
        "pmid": s["uid"],
        "title": (s.get("title") or "").rstrip(". "),
        "authors": ", ".join(a["name"] for a in s.get("authors", []) if a.get("authtype") == "Author"),
        "journal": s.get("fulljournalname") or s.get("source") or "",
        "journal_abbrev": s.get("source") or "",
        "year": int(year_match.group()) if year_match else 0,
        "volume": s.get("volume") or "",
        "issue": s.get("issue") or "",
        "pages": s.get("pages") or "",
        "doi": ids.get("doi", ""),
        "pmcid": ids.get("pmc", ""),
        "type": "review" if "Review" in pubtypes else ("comment" if any(t in pubtypes for t in ("Comment", "Editorial")) else "article"),
        "sortdate": s.get("sortpubdate", ""),
    }
    # Remove HTML tags PubMed sometimes leaves in titles (e.g. <i>)
    rec["title"] = re.sub(r"</?\w+>", "", rec["title"])
    return rec


PREPRINT_SERVERS = {"biorxiv", "medrxiv", "arxiv", "research square", "ssrn"}
NOTICE = re.compile(r"^(author correction|correction|erratum|retraction|publisher correction)\b", re.I)


def norm(title):
    return re.sub(r"[^a-z0-9 ]", "", title.lower())


def first_author(r):
    return r["authors"].split(",")[0].split(" ")[0].lower() if r["authors"] else ""


def clean(records):
    """Drop correction notices, and preprints whose published version is also listed."""
    records = [r for r in records if not NOTICE.match(r["title"])]
    for r in records:
        r["preprint"] = r["journal_abbrev"].lower() in PREPRINT_SERVERS
    published = [r for r in records if not r["preprint"]]
    kept = []
    for r in records:
        if r["preprint"] and any(
            first_author(p) == first_author(r)
            and difflib.SequenceMatcher(None, norm(p["title"]), norm(r["title"])).ratio() > 0.8
            for p in published
        ):
            continue
        kept.append(r)
    return kept


def main():
    pmids = search_pmids()
    print(f"PubMed returned {len(pmids)} records for {QUERY!r}")
    records = clean([to_record(s) for s in summarize(pmids)])
    records.sort(key=lambda r: (r["sortdate"], r["pmid"]), reverse=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(records, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(records)} publications to {OUT.relative_to(OUT.parent.parent)}")


if __name__ == "__main__":
    main()
