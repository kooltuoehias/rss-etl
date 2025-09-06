import spacy
from dateutil import parser
from typing import List, Dict

# Load spaCy model once
nlp = spacy.load("en_core_web_sm")

# Define simple keyword-based domain classifier
DOMAIN_KEYWORDS = {
    "oncology": ["cancer", "tumor", "chemotherapy"],
    "cardiology": ["heart", "cardiac", "stroke"],
    "neurology": ["brain", "neuro", "alzheimer"],
    "infectious disease": ["covid", "virus", "vaccine", "flu"],
    "hematology": ["sickle cell", "blood", "hemoglobin"]
}

def classify_domain(text: str) -> str:
    lowered = text.lower()
    for domain, keywords in DOMAIN_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return domain
    return "general"

def transform_articles(raw_articles: List[Dict]) -> List[Dict]:
    transformed = []

    for article in raw_articles:
        # Normalize date
        raw_date = article.get("published", "")
        if "EDT" in raw_date:
            raw_date = raw_date.replace("EDT", "-0400")
        published_dt = parser.parse(raw_date)

        # NLP enrichment
        doc = nlp(article.get("summary", ""))
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        # Classify domain
        domain = classify_domain(article.get("title", "") + " " + article.get("summary", ""))

        transformed.append({
            "title": article.get("title"),
            "url": article.get("link"),
            "published": published_dt.isoformat(),
            "source": article.get("source"),
            "summary": article.get("summary"),
            "category": domain,
            "entities": entities  # Optional: store or use later
        })

    return transformed

