import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

BASE_URL = "https://www.bisnis.com"


def fetch_article(link):

    print(f"Scraping {link}")
    res = requests.get(link)
    if res.status_code != 200:
        print(f"Gagal fetch {link}, status: {res.status_code}")
        return None

    soup = BeautifulSoup(res.text, "html.parser")

    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else None

    paragraphs = soup.find_all("p")
    content = " ".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

    published_at = None
    meta_date = soup.find("meta", attrs={"name": "publishdate"})
    if meta_date and meta_date.get("content"):
        raw_date = meta_date["content"]  
        print(f"Raw tanggal: {raw_date}")
        try:
            dt_obj = datetime.strptime(raw_date, "%Y/%m/%d %H:%M:%S")
            published_at = dt_obj.isoformat() + "+07:00"  # WIB
        except Exception as e:
            print(f"Gagal parse meta publishdate '{raw_date}': {e}")
    else:
        print("Tidak ada publishdate.")

    return {
        "link": link,
        "title": title,
        "content": content,
        "published_at": published_at
    }


def fetch_articles_listing(page=1):

    url = f"{BASE_URL}/?page={page}"
    print(f"[DEBUG] Mengambil page {page}: {url}")
    res = requests.get(url)
    if res.status_code != 200:
        print(f"[DEBUG] Gagal {page}, status: {res.status_code}")
        return []
    soup = BeautifulSoup(res.text, "html.parser")

    links = set()
    for a in soup.select("a"):
        href = a.get("href")
        if not href:
            continue
        if "/read/" in href:  
            if href.startswith("/"):
                full = BASE_URL + href
            else:
                full = href
            links.add(full)

    links = list(links)
    print(f"[DEBUG] Terdapat {len(links)} artikel di page {page}")
    return links


def backtrack(start_date, end_date, output_file="backtrack.json"):
    start_date = datetime.strptime(start_date, "%d-%m-%Y")
    end_date = datetime.strptime(end_date, "%d-%m-%Y")
    end_date = end_date.replace(hour=23, minute=59, second=59)

    first = True
    page = 1

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("[\n")

    while True:
        links = fetch_articles_listing(page)
        if not links:
            break

        stop = False
        for i, link in enumerate(links, start=1):
            print(f"\n[ITERASI] Page {page}, Artikel {i}/{len(links)}")
            data = fetch_article(link)
            if data is None or data["published_at"] is None:
                print(f"[SKIP] Tidak ada tanggal: {link}")
                continue

            pub_date = datetime.fromisoformat(data["published_at"].replace("+07:00", ""))

            if start_date <= pub_date <= end_date:
                with open(output_file, "a", encoding="utf-8") as f:
                    if not first:
                        f.write(",\n")
                    json.dump(data, f, ensure_ascii=False)
                    first = False
                print(f"[SAVED] {data['title']}")
            elif pub_date < start_date:
                stop = True
                continue
            else:
                stop = False
                print(f"[SKIP] {data['title']}")

        if stop:
            break
        page += 1

    with open(output_file, "a", encoding="utf-8") as f:
        f.write("\n]")
