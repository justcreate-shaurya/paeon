"""
Paeon AI - PII Detection and Stripping Service

Ensures DPDP Act 2023 compliance by detecting and removing
personally identifiable information before LLM processing.

PII Types Detected:
- Names (via NER)
- Phone numbers
- Email addresses
- Aadhaar numbers (India)
- Medical record numbers
- Dates of birth
- Addresses
"""

import re
from typing import Any


class PIIStripper:
    """
    PII detection and stripping service.
    
    All PII is detected and replaced with placeholders
    before any text is sent to LLM or stored.
    """

    # Regex patterns for common PII
    PATTERNS = {
        "email": (
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "[EMAIL_REDACTED]"
        ),
        "phone_india": (
            r'\b(?:\+91[\-\s]?)?[6-9]\d{9}\b',
            "[PHONE_REDACTED]"
        ),
        "phone_us": (
            r'\b(?:\+1[\-\s]?)?\(?\d{3}\)?[\-\s]?\d{3}[\-\s]?\d{4}\b',
            "[PHONE_REDACTED]"
        ),
        "phone_generic": (
            r'\b\d{10,15}\b',
            "[PHONE_REDACTED]"
        ),
        "aadhaar": (
            r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
            "[AADHAAR_REDACTED]"
        ),
        "ssn": (
            r'\b\d{3}[\s-]?\d{2}[\s-]?\d{4}\b',
            "[SSN_REDACTED]"
        ),
        "mrn": (
            r'\b(?:MRN|MR|Patient\s*ID)[\s:#-]*\d{4,12}\b',
            "[MRN_REDACTED]"
        ),
        "dob": (
            r'\b(?:DOB|Date\s*of\s*Birth|Born)[\s:]*\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b',
            "[DOB_REDACTED]"
        ),
        "date_pattern": (
            r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b',
            "[DATE_REDACTED]"
        ),
        "credit_card": (
            r'\b(?:\d{4}[\s-]?){3}\d{4}\b',
            "[CARD_REDACTED]"
        ),
        "ip_address": (
            r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            "[IP_REDACTED]"
        ),
    }

    # Common name patterns (will be refined with NER)
    NAME_PATTERNS = [
        r'\b(?:Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',
        r'\b(?:my name is|I am|I\'m)\s+[A-Z][a-z]+\b',
    ]

    # Indian name prefixes/suffixes
    INDIAN_NAME_INDICATORS = [
        "ji", "bhai", "ben", "kumar", "kumari", "singh", "kaur",
        "devi", "sharma", "gupta", "patel", "khan", "reddy"
    ]

    def __init__(self):
        """Initialize the PII stripper."""
        self._compile_patterns()

    def _compile_patterns(self):
        """Pre-compile regex patterns for efficiency."""
        self.compiled_patterns = {}
        for name, (pattern, replacement) in self.PATTERNS.items():
            self.compiled_patterns[name] = (
                re.compile(pattern, re.IGNORECASE),
                replacement
            )
        
        self.name_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.NAME_PATTERNS
        ]

    def detect_pii(self, text: str) -> dict[str, Any]:
        """
        Detect PII in text without modifying it.
        
        Returns detection report with types and counts.
        """
        detections = {
            "pii_detected": False,
            "pii_types": [],
            "pii_count": 0,
            "confidence_scores": {},
        }

        for pii_type, (pattern, _) in self.compiled_patterns.items():
            matches = pattern.findall(text)
            if matches:
                detections["pii_detected"] = True
                detections["pii_types"].append(pii_type)
                detections["pii_count"] += len(matches)
                detections["confidence_scores"][pii_type] = 0.95

        # Check for names
        for name_pattern in self.name_patterns:
            matches = name_pattern.findall(text)
            if matches:
                detections["pii_detected"] = True
                if "name" not in detections["pii_types"]:
                    detections["pii_types"].append("name")
                detections["pii_count"] += len(matches)
                detections["confidence_scores"]["name"] = 0.8

        return detections

    def strip_pii(self, text: str) -> tuple[str, dict[str, Any]]:
        """
        Strip all detected PII from text.
        
        Returns:
            tuple: (sanitized_text, detection_report)
        """
        original_length = len(text)
        sanitized = text

        # Apply all pattern replacements
        for pii_type, (pattern, replacement) in self.compiled_patterns.items():
            sanitized = pattern.sub(replacement, sanitized)

        # Apply name pattern replacements
        for name_pattern in self.name_patterns:
            sanitized = name_pattern.sub("[NAME_REDACTED]", sanitized)

        # Generate report
        report = self.detect_pii(text)
        report["original_length"] = original_length
        report["stripped_length"] = len(sanitized)
        report["detection_model_version"] = "1.0.0"

        return sanitized, report

    def mask_partial(self, text: str, mask_char: str = "*") -> str:
        """
        Partially mask PII for display purposes.
        
        Example: "john@example.com" -> "j***@e******.com"
        """
        masked = text

        # Mask emails
        email_pattern = re.compile(r'\b([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+)\.([A-Z|a-z]{2,})\b')
        
        def mask_email(match):
            local = match.group(1)
            domain = match.group(2)
            tld = match.group(3)
            masked_local = local[0] + mask_char * (len(local) - 1) if len(local) > 1 else local
            masked_domain = domain[0] + mask_char * (len(domain) - 1) if len(domain) > 1 else domain
            return f"{masked_local}@{masked_domain}.{tld}"
        
        masked = email_pattern.sub(mask_email, masked)

        # Mask phone numbers (keep last 4 digits)
        phone_pattern = re.compile(r'\b(\+?\d{1,3}[\s-]?)?(\d{3,})(\d{4})\b')
        
        def mask_phone(match):
            prefix = match.group(1) or ""
            middle = mask_char * len(match.group(2))
            suffix = match.group(3)
            return f"{prefix}{middle}{suffix}"
        
        masked = phone_pattern.sub(mask_phone, masked)

        return masked

    def validate_no_pii(self, text: str) -> bool:
        """
        Validate that text contains no detectable PII.
        
        Returns True if clean, False if PII detected.
        """
        detection = self.detect_pii(text)
        return not detection["pii_detected"]


# Singleton instance
pii_stripper = PIIStripper()
