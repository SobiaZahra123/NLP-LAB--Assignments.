## Pakistan Agencies NLP Dataset
A structured NLP dataset built from Wikipedia covering 80+ official agencies,
departments, and organisations of Pakistan scraped, cleaned, and merged
into a single master CSV for research and machine learning use
### Objective
Build a custom NLP dataset by scraping Wikipedia pages for 80+ Pakistani government
agencies, saving individual text files, then merging them into a single master CSV.

### Workflow

| Step | Description | Output |
| 1 | Scrape each agency's Wikipedia page | `agency_files/inter-services_intelligence.txt
| 2 | Merge all individual files | `pakistan_agencies_dataset.csv

### Dataset Details

| Field          | Value |
|----------------|-------|
| Source         | English Wikipedia |
| Total Agencies | 80+   |
| Categories     | Intelligence, Military, Finance, Health, Education, Energy, Transport, Media, Legal |
| Features       | agency_slug, agency_name, text, char_count, word_count |
| Format         | CSV (master) + TXT (individual) |
| Max text/agency| 5,000 characters |
| Language       | English |

### Agency Categories Covered

- Intelligence & Security: ISI, IB, FIA, MI, NACTA
- Military & Defence: Pakistan Army, Navy, Air Force, JCS
- Nuclear & Space: PAEC, KRL, SUPARCO, PNRA
- Finance & Economy: SBP, FBR, PSX, SECP
- Health: DRAP, PIMS, NIH, PMC
- Education & Research: HEC, PCSIR, Pakistan Academy of Sciences
- Energy & Environment: NEPRA, WAPDA, AEDB, OGDC
- Communications & Tech: PTA, PTCL, NITB, PEMRA
- Transport: Pakistan Railways, PIA, CAA, NHA
- Social & Welfare: BISP, NADRA, EOBI
- Media & Culture: PBC, PTV, APP, PNCA
- Judicial & Legal: Supreme Court, NAB, FTO
- Agriculture: PARC, ADBP
- Housing & Development: CDA, LDA, KDA

### How to Run
pip install requests beautifulsoup4
python nlp_pakistan_agencies_scraper.py

### Kaggle Dataset

View Dataset on Kaggle
https://www.kaggle.com/datasets/sobiamatthal/pakistan-government-agencies-dataset
