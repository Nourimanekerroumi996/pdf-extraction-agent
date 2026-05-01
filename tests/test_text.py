from app.extractors.text import extract_text

def test_extract_text():
    text, pages = extract_text("tests/fixtures/sample.pdf")
    assert pages > 0
    assert len(text) > 0