# PubMed Paper Fetcher

This CLI tool fetches research papers from PubMed based on a user query, and filters papers that have at least one author affiliated with a pharmaceutical or biotech company.

## How to Use

### 1. ## ✅ Requirements

- **Python 3.8+**
- **Poetry** (for dependency management)

  ### 2. ### 🔧 Install Python

Download and install from:  
https://www.python.org/downloads/


### 4. Install Poetry

Run this command in PowerShell or Terminal:

```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
Then restart your terminal and verify:
poetry --version

### 5. Without Poetry
pip install requests
python get_papers_list.py "cancer research" -f cancer_results.csv -d

### 6. With Poetry
python -m poetry install 
poetry run python get_papers_list.py "cancer research" -f cancer_results.csv -d





