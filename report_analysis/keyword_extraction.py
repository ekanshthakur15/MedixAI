# keyword_extraction.py

import spacy

# Load a pre-trained spaCy model (this is for general-purpose NER)
nlp = spacy.load("en_core_web_sm")


def extract_keywords_from_reports(reports):
    """
    Extract relevant keywords from multiple medical reports.
    """
    keywords = set()
    for report in reports:
        doc = nlp(report.report_content)  # Process each report's content

        # Extract named entities (e.g., medical conditions, diseases)
        for ent in doc.ents:
            if ent.label_ in ['DISEASE', 'SYMPTOM', 'MEDICAL_CONDITION']:
                keywords.add(ent.text.lower())

        # Optionally, add a list of medical terms or conditions manually
        additional_keywords = ["diabetes",
                               "hypertension", "asthma", "heart disease"]
        keywords.update(additional_keywords)

    return list(keywords)
