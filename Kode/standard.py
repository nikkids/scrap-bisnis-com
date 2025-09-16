import sys
import json
import time
from datetime import datetime
from bisnis_crawler import fetch_articles_listing, fetch_article

def standard(interval=60, output_file="hasil_standard.json"):
    seen = set()
    first = True 

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("[\n")  

    try:
        while True:
            links = fetch_articles_listing(1)
            for link in links:
                if link not in seen:
                    data = fetch_article(link)
                    if data and data["title"] and data["published_at"]:
                        with open(output_file, "a", encoding="utf-8") as f:
                            if not first:
                                f.write(",\n")  
                            f.write(json.dumps(data, ensure_ascii=False, indent=2))
                            first = False

                        print(f"[{datetime.now().isoformat()}] Artikel baru tersimpan: {data['title'][:60]}")
                        seen.add(link)

            time.sleep(interval)

    except KeyboardInterrupt:
        with open(output_file, "a", encoding="utf-8") as f:
            f.write("\n]\n")


if __name__ == "__main__":
    interval = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    output_file = sys.argv[2] if len(sys.argv) > 2 else "hasil_standard.json"

    standard(interval=interval, output_file=output_file)
