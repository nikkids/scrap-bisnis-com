import sys
import json
from bisnis_crawler import backtrack

if __name__ == "__main__":
    if len(sys.argv) < 3:

        sys.exit(1)

    start_date = sys.argv[1]
    end_date = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else "hasil.json"

    backtrack(start_date, end_date, output_file)

    try:
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"\n Terdapat {len(data)} artikel")

        if data:
            sample = data[0]
            print("\nContoh artikel:")
            print(f"- Judul       : {sample['title']}")
            print(f"- Link        : {sample['link']}")
            print(f"- Published   : {sample['published_at']}")
            print(f"- Cuplikan isi: {sample['content'][:150]}...")
    except Exception as e:
        print(f"Gagal baca hasil: {e}")
