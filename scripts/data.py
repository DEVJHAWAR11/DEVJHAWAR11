"""GitHub numbers for the profile graphics.

With GITHUB_TOKEN (or GH_TOKEN) set, fetches fresh data and caches it in scripts/data.json.
Without a token, the cached copy is used so the graphics can still be rebuilt offline.
"""
import json
import os
import urllib.request
from pathlib import Path

USER = "DEVJHAWAR11"
CACHE = Path(__file__).resolve().parent / "data.json"
SKIP_LANGS = {"Jupyter Notebook", "HTML", "CSS", "Batchfile", "PowerShell", "Shell", "Dockerfile", "TSQL"}

QUERY = """
query($login: String!, $merged: String!, $opened: String!) {
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions
      contributionCalendar { totalContributions weeks { contributionDays { contributionCount } } }
    }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes { languages(first: 8, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } }
    }
  }
  merged: search(query: $merged, type: ISSUE, first: 100) {
    nodes { ... on PullRequest { title repository { nameWithOwner stargazerCount } } }
  }
  opened: search(query: $opened, type: ISSUE, first: 1) { issueCount }
}
"""


def _fetch(token):
    variables = {"login": USER,
                 "merged": f"author:{USER} is:pr is:merged -user:{USER}",
                 "opened": f"author:{USER} is:pr -user:{USER}"}
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = json.load(r)
    if "errors" in raw:
        raise SystemExit(raw["errors"])
    d = raw["data"]
    cc = d["user"]["contributionsCollection"]
    days = [day["contributionCount"] for w in cc["contributionCalendar"]["weeks"] for day in w["contributionDays"]]

    longest = run = 0
    for c in days:
        run = run + 1 if c else 0
        longest = max(longest, run)

    sizes = {}
    for repo in d["user"]["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            name = e["node"]["name"]
            if name not in SKIP_LANGS:
                sizes[name] = sizes.get(name, 0) + e["size"]
    total = sum(sizes.values()) or 1
    langs = [[n, round(v * 100 / total, 1)] for n, v in sorted(sizes.items(), key=lambda kv: -kv[1])[:6]]

    merged = [{"repo": p["repository"]["nameWithOwner"], "stars": p["repository"]["stargazerCount"], "title": p["title"]}
              for p in d["merged"]["nodes"] if p]
    merged.sort(key=lambda p: (-p["stars"], p["repo"], p["title"]))

    return {"contributions": cc["contributionCalendar"]["totalContributions"],
            "commits": cc["totalCommitContributions"], "longest_streak": longest, "days": days,
            "repos": d["user"]["repositories"]["totalCount"], "langs": langs,
            "merged": merged, "opened": d["opened"]["issueCount"]}


def load():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        data = _fetch(token)
        CACHE.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        return data
    return json.loads(CACHE.read_text(encoding="utf-8"))
