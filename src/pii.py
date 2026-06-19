from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
#load engines
_analyzer=AnalyzerEngine()
_anonymizer=AnonymizerEngine()
ENTITIES = [
    "PERSON",
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "CREDIT_CARD",
    "IP_ADDRESS",
    "US_SSN",
]
def redact(text: str) -> str:
    """
    Scans text for PII and replaces sensitive spans with placeholders.
    Example: "Contact John at john@co.com" -> "Contact <PERSON> at <EMAIL_ADDRESS>"
    Non-sensitive text is preserved exactly as is.
    """
    if not text or not text.strip():
        return text

    # Step 1: Find all PII spans in the text
    results = _analyzer.analyze(
        text=text,
        entities=ENTITIES,
        language="en",
    )

    # Step 2: Replace found spans with placeholders
    anonymized = _anonymizer.anonymize(
        text=text,
        analyzer_results=results,
    )

    return anonymized.text