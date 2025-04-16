import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from compliance import check_gdpr_compliance

def test_compliance_check():
    result = check_gdpr_compliance("https://example.com")
    assert isinstance(result, dict)
    assert "cookie_banner" in result
    assert "privacy_policy" in result
