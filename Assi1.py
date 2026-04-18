import os
import time
import csv
import requests
from bs4 import BeautifulSoup

AGENCIES = [
    # Intelligence & Security
    "Inter-Services_Intelligence",
    "Intelligence_Bureau_(Pakistan)",
    "Military_Intelligence_(Pakistan)",
    "Federal_Investigation_Agency",
    "National_Counter_Terrorism_Authority",
    "Strategic_Plans_Division",

    # Law Enforcement
    "Pakistan_Police",
    "Pakistan_Rangers",
    "Frontier_Corps",
    "Pakistan_Coast_Guards",
    "Airport_Security_Force",
    "National_Highways_and_Motorway_Police",
    "Islamabad_Capital_Territory_Police",

    # Military & Defence
    "Pakistan_Army",
    "Pakistan_Navy",
    "Pakistan_Air_Force",
    "Joint_Chiefs_of_Staff_Committee_(Pakistan)",
    "Pakistan_Ordnance_Factories",
    "Defence_Housing_Authority",
    "National_Logistics_Cell",

    # Nuclear & Space
    "Pakistan_Atomic_Energy_Commission",
    "Khan_Research_Laboratories",
    "Pakistan_Space_and_Upper_Atmosphere_Research_Commission",
    "Pakistan_Nuclear_Regulatory_Authority",

    # Finance & Economy
    "State_Bank_of_Pakistan",
    "Securities_and_Exchange_Commission_of_Pakistan",
    "Federal_Board_of_Revenue_(Pakistan)",
    "National_Bank_of_Pakistan",
    "Pakistan_Stock_Exchange",
    "Economic_Coordination_Committee",
    "Board_of_Investment_(Pakistan)",
    "Competition_Commission_of_Pakistan",

    # Health
    "Drug_Regulatory_Authority_of_Pakistan",
    "Pakistan_Institute_of_Medical_Sciences",
    "National_Institute_of_Health_(Pakistan)",
    "Pakistan_Medical_Commission",

    # Education & Research
    "Higher_Education_Commission_(Pakistan)",
    "Pakistan_Council_of_Scientific_and_Industrial_Research",
    "Pakistan_Standards_and_Quality_Control_Authority",
    "National_Library_of_Pakistan",
    "Pakistan_Academy_of_Sciences",

    # Energy & Environment
    "Oil_and_Gas_Development_Company",
    "Pakistan_Petroleum_Limited",
    "National_Electric_Power_Regulatory_Authority",
    "Alternative_Energy_Development_Board",
    "Pakistan_Environmental_Protection_Agency",
    "Water_and_Power_Development_Authority",
    "Pakistan_Meteorological_Department",

    # Communications & Technology
    "Pakistan_Telecommunication_Authority",
    "Pakistan_Telecommunication_Company_Limited",
    "National_Telecommunication_Corporation",
    "Pakistan_Software_Export_Board",
    "National_Information_Technology_Board",
    "Electronic_Media_Regulatory_Authority",

    # Transport & Infrastructure
    "Pakistan_Railways",
    "Pakistan_International_Airlines",
    "Civil_Aviation_Authority_(Pakistan)",
    "National_Highway_Authority_(Pakistan)",
    "Karachi_Port_Trust",
    "Port_Qasim_Authority",
    "Gwadar_Port_Authority",

    # Social & Welfare
    "Benazir_Income_Support_Programme",
    "National_Database_and_Registration_Authority",
    "Employees_Old-Age_Benefits_Institution",
    "Pakistan_Bait_ul_Mal",
    "Zakat_and_Ushr_Department",
    "Pakistan_Red_Crescent_Society",

    # Media & Culture
    "Pakistan_Broadcasting_Corporation",
    "Pakistan_Television_Corporation",
    "Associated_Press_of_Pakistan",
    "Pakistan_National_Council_of_the_Arts",
    "Directorate_General_of_Films_and_Publications",
    "Pakistan_Tourism_Development_Corporation",

    # Judicial & Legal
    "Supreme_Court_of_Pakistan",
    "Federal_Shariat_Court",
    "National_Accountability_Bureau",
    "Federal_Tax_Ombudsman",
    "Wafaqi_Mohtasib",

    # Agriculture & Food
    "Pakistan_Agricultural_Research_Council",
    "Agriculture_Development_Bank_of_Pakistan",
    "Pakistan_Oilseed_Development_Board",
    "Trading_Corporation_of_Pakistan",

    # Housing & Development
    "Capital_Development_Authority",
    "Lahore_Development_Authority",
    "Karachi_Development_Authority",
    "Federal_Government_Employees_Housing_Foundation",
]
OUTPUT_DIR  = "agency_files"
MASTER_FILE = "pakistan_agencies_dataset.csv"
WIKI_BASE   = "https://en.wikipedia.org/wiki/"
HEADERS     = {"User-Agent": "Mozilla/5.0 (NLP-Lab-Assignment/1.0)"}
DELAY       = 1.0          # seconds between requests
MAX_CHARS   = 5000

def scrape_page(slug: str) -> str:
    """Fetch a Wikipedia page and return cleaned paragraph text."""
    url = WIKI_BASE + slug
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            print(f"    [WARN] HTTP {resp.status_code} — {slug}")
            return ""

        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove noise
        for tag in soup(["sup", "table", "style", "script",
                          "nav", "footer", "aside"]):
            tag.decompose()

        content = soup.find("div", {"id": "mw-content-text"})
        if not content:
            return ""

        paras = content.find_all("p")
        text  = " ".join(
            p.get_text(separator=" ", strip=True)
            for p in paras
            if len(p.get_text(strip=True)) > 50
        )
        return " ".join(text.split())[:MAX_CHARS]

    except Exception as e:
        print(f"    [ERROR] {slug}: {e}")
        return ""


def save_individual_files():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    success, failed = 0, []

    print(f"\n{'='*65}")
    print(f"  STEP 1 — Scraping {len(AGENCIES)} Pakistan agencies from Wikipedia")
    print(f"{'='*65}")

    for i, slug in enumerate(AGENCIES, 1):
        display_name = slug.replace("_", " ")
        safe_name    = slug.lower() + ".txt"
        filepath     = os.path.join(OUTPUT_DIR, safe_name)

        if os.path.exists(filepath):
            print(f"  [{i:3d}/{len(AGENCIES)}] SKIP  {display_name}")
            success += 1
            continue

        print(f"  [{i:3d}/{len(AGENCIES)}] Scraping: {display_name}")
        text = scrape_page(slug)

        if text:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Agency: {display_name}\n")
                f.write("=" * 65 + "\n")
                f.write(text + "\n")
            success += 1
            print(f"           Saved {len(text):,} chars → {safe_name}")
        else:
            failed.append(slug)
            print(f"           [FAILED] No content found.")

        time.sleep(DELAY)

    print(f"\n  Completed. Success: {success} | Failed: {len(failed)}")
    if failed:
        print(f"  Failed slugs: {failed}")


def merge_to_master():
    print(f"\n{'='*65}")
    print(f"  STEP 2 — Merging into {MASTER_FILE}")
    print(f"{'='*65}")

    txt_files = sorted(f for f in os.listdir(OUTPUT_DIR) if f.endswith(".txt"))

    if not txt_files:
        print("  [ERROR] No .txt files found. Run Step 1 first.")
        return

    with open(MASTER_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=["agency_slug", "agency_name", "text", "char_count", "word_count"]
        )
        writer.writeheader()

        for fname in txt_files:
            slug        = fname.replace(".txt", "")
            agency_name = slug.replace("_", " ").title()
            fpath       = os.path.join(OUTPUT_DIR, fname)

            with open(fpath, "r", encoding="utf-8") as f:
                lines = f.readlines()
                body  = "".join(lines[2:]).strip()   # skip header lines

            writer.writerow({
                "agency_slug": slug,
                "agency_name": agency_name,
                "text":        body,
                "char_count":  len(body),
                "word_count":  len(body.split()),
            })
            print(f"  Merged: {agency_name:<55} ({len(body):,} chars)")

    print(f"\n  Master CSV saved → {MASTER_FILE}")
    print(f"  Total agencies   : {len(txt_files)}")

if __name__ == "__main__":
    save_individual_files()
    merge_to_master()

    print("\n" + "="*65)
    print("  ALL DONE!")
    print(f"  Individual files → ./{OUTPUT_DIR}/")
    print(f"  Master dataset   → ./{MASTER_FILE}")
    print("  Next: upload both to GitHub (NLP-LAB-Assignments) & Kaggle.")
    print("="*65)