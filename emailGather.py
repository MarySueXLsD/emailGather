#!/usr/bin/env python3
"""emailGather.py – minimal e‑mail crawler.
Run: python3 emailGather.py and follow the prompts.
"""

import re, sys, time, urllib.parse
from collections import deque
from datetime import timedelta

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
#  ASCII bird logo (prints on launch)
# ---------------------------------------------------------------------------

BIRD = r"""
           (                           )
      ) )( (                           ( ) )( (
       ( ( ( )  ) )                     ( (   (  ) )(
      ) )     ,,''\                     ///,,       ) (
   (  ((    (;;;;//                     ;;////)      )
    ) )    (-(__//                       ;;__)-)     (
   (((   ((-(__||                         ||__)-))    ) )
  ) )   ((-(-(_||           ```\__        ||_)-)-))   ((
  ((   ((-(-(/(/;;        ''; 9.- `      //\)\)-)-))    )
   )   (-(-(/(/(/;;      '';;;;-\~      //\)\)\)-)-)   (   )
(  (   ((-(-(/(/(/\======,:;:;:;:,======/\)\)\)-)-))   )
    )  '(((-(/(/(/(//////:%%%%%%%:;;;;;;)\)\)\)-)))`  ( (
   ((   '((-(/(/(/('uuuu:WWWWWWWWW:uuuu`)\)\)\)-))`    )
     ))  '((-(/(/(/('|||:wwwwwwwww:|||')\)\)\)-))`    ((
  (   ((   '((((/(/('uuu:WWWWWWWWW:uuu`)\)\))))`     ))
    ))   '':::UUUUUU:wwwwwwwww:UUUUUU:::``     ((   )
      ((      '''''''-uuuuuuuu/``````         ))
       ))            `JJJJJJJJJ`            ((
         ((            LLLLLLLLLLL         ))
           ))         ///|||||||;;\       ((
             ))      (/(/(/(^)\)\)       ((
              ((                           ))
                ((                       ((
                  ( )( ))( ( ( ) )( ) (()
"""

EMAIL_RE = re.compile(r"[a-z0-9.\-_+]+@[a-z0-9.\-_]+\.[a-z]+", re.I)


def show_banner():
    """Print the ASCII bird logo."""
    print(BIRD)
    print("emailGather – quick email scraper\n")


def gather(root_url, limit):
    """Crawl *limit* pages starting from *root_url* and return a set of e‑mails."""
    urls = deque([root_url])
    visited = set()
    emails = set()
    start = time.monotonic()

    while urls and len(visited) < limit:
        url = urls.popleft()
        if url in visited:
            continue
        visited.add(url)
        print(f"[{len(visited):>4}] {url}")

        try:
            resp = requests.get(url, timeout=10, headers={"User-Agent": "emailGather/1.0"})
        except requests.RequestException:
            continue

        emails.update(EMAIL_RE.findall(resp.text))

        soup = BeautifulSoup(resp.text, "lxml")
        base = f"{urllib.parse.urlsplit(url).scheme}://{urllib.parse.urlsplit(url).netloc}"
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("mailto:"):
                continue
            if href.startswith("/"):
                href = base + href
            elif not href.startswith("http"):
                href = urllib.parse.urljoin(url, href)
            if href not in visited:
                urls.append(href)

    duration = timedelta(seconds=time.monotonic() - start)
    print(f"\nFinished in {duration}. Found {len(emails)} unique e‑mails:\n")
    for addr in sorted(emails):
        print(addr)

    filename = (
        root_url.replace("https://", "")
        .replace("http://", "")
        .replace(".", "_")
        + "_emails.txt"
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(emails)))
    print(f"\nSaved to {filename}")


if __name__ == "__main__":
    try:
        show_banner()
        root = input("Root URL (e.g. https://example.com): ").strip()
        max_pages = input("Maximum pages to scan [200]: ").strip() or "200"
        gather(root, int(max_pages))
    except KeyboardInterrupt:
        sys.exit("\nCancelled by user.")
