
from docs2prompt.token_optimizer import (
    remove_extra_whitespace,
    standardize_line_breaks,
    remove_redundant_headers,
)

def test_remove_extra_whitespace():
    content = "  This   is  a  test  string  with  extra  whitespace.  "
    expected = "This is a test string with extra whitespace."
    assert remove_extra_whitespace(content) == expected

def test_standardize_line_breaks():
    content = "Line1\r\nLine2\rLine3\nLine4"
    expected = "Line1\nLine2\nLine3\nLine4"
    assert standardize_line_breaks(content) == expected

def test_remove_redundant_headers():
    content = "# Header\nContent\n# Header\nMore Content"
    expected = "# Header\nContent\nMore Content"
    assert remove_redundant_headers(content) == expected

