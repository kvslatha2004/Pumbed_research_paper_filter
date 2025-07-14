import requests
import csv
import argparse
from typing import List, Dict
from xml.etree import ElementTree as ET


def fetch_pubmed_ids(query: str) -> List[str]:
    """Get PubMed IDs based on search query."""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    response = requests.get(url, params={
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 10
    })
    response.raise_for_status()
    return response.json()['esearchresult']['idlist']


def fetch_paper_details(pubmed_id: str) -> Dict[str, str]:
    """Fetch detailed paper info using efetch."""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    response = requests.get(url, params={
        "db": "pubmed",
        "id": pubmed_id,
        "retmode": "xml"
    })
    root = ET.fromstring(response.content)

    title = root.findtext(".//ArticleTitle", default="N/A")
    date = root.findtext(".//PubDate/Year", default="N/A")

    authors = root.findall(".//Author")
    company_affiliations = []
    non_academic_authors = []
    email = ""

    for author in authors:
        affil = author.findtext(".//Affiliation")
        if affil and any(x in affil.lower() for x in ["pharma", "biotech", "therapeutics", "labs", "inc", "ltd"]):
            company_affiliations.append(affil)
            lastname = author.findtext("LastName", "")
            non_academic_authors.append(lastname)
            if "@" in affil:
                email = affil.split()[-1]

    return {
        "PubmedID": pubmed_id,
        "Title": title,
        "Publication Date": date,
        "Non-academic Author(s)": ", ".join(non_academic_authors),
        "Company Affiliation(s)": ", ".join(company_affiliations),
        "Corresponding Author Email": email
    } if non_academic_authors else {}


def write_to_csv(papers: List[Dict[str, str]], filename: str):
    """Write paper details to CSV."""
    with open(filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "PubmedID", "Title", "Publication Date",
            "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"
        ])
        writer.writeheader()
        for row in papers:
            writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with pharma/biotech affiliations.")
    parser.add_argument("query", type=str, help="Search query")
    parser.add_argument("-f", "--file", type=str, help="CSV output filename", default="results.csv")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    ids = fetch_pubmed_ids(args.query)
    if args.debug:
        print(f"Found PubMed IDs: {ids}")

    results = []
    for pid in ids:
        paper = fetch_paper_details(pid)
        if paper:
            results.append(paper)
            if args.debug:
                print(f"Added paper: {paper['Title']}")

    write_to_csv(results, args.file)
    print(f"{len(results)} papers written to {args.file}")


if __name__ == "__main__":
    main()
