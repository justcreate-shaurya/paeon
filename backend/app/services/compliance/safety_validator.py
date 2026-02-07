"""
Paeon AI - Safety Validator Service

Ensures all AI outputs comply with medical safety constraints.

The system must NEVER:
1. Diagnose conditions
2. Prescribe treatments
3. Recommend medications
4. Make prognosis statements
5. Provide unsolicited medical advice

This validator catches and sanitizes any unsafe outputs.
"""

import re
from typing import Any


class SafetyValidator:
    """
    Medical safety validation for AI outputs.
    
    Implements guardrails to ensure outputs are:
    - Descriptive (symptom terminology) not diagnostic
    - Educational not prescriptive
    - Sourced and verifiable
    """

    # Diagnostic language patterns (BLOCKED)
    DIAGNOSTIC_PATTERNS = [
        r'\byou have\b.*(?:disease|disorder|condition|syndrome|infection)',
        r'\byou are suffering from\b',
        r'\bdiagnosis:?\s*(?:is|would be|appears to be)',
        r'\bthis (?:is|indicates|suggests|confirms)\s+(?:a|an)?\s*(?:disease|disorder|condition)',
        r'\byou(?:\'ve| have) (?:got|contracted|developed)\b',
        r'\btest results (?:show|indicate|confirm) (?:you have|presence of)',
    ]

    # Prescriptive language patterns (BLOCKED)
    PRESCRIPTIVE_PATTERNS = [
        r'\byou should take\b',
        r'\btake\s+\d+\s*(?:mg|ml|tablets?|pills?|capsules?)',
        r'\bI (?:recommend|suggest|advise) (?:you take|taking)',
        r'\bprescription:?\s*',
        r'\bstart (?:taking|on|with)\s+\w+\s*(?:mg|ml)?',
        r'\byou need\s+(?:to take|medication|medicine|treatment)',
        r'\bdosage:?\s*\d+',
    ]

    # Prognosis language patterns (BLOCKED)
    PROGNOSIS_PATTERNS = [
        r'\bthis will\s+(?:get|become|turn|progress)',
        r'\byour condition will\b',
        r'\bexpect\s+(?:recovery|improvement|deterioration)',
        r'\blikely to\s+(?:recover|worsen|die|survive)',
        r'\bprognosis:?\s*',
        r'\blife expectancy\b',
    ]

    # Treatment recommendation patterns (BLOCKED)
    TREATMENT_PATTERNS = [
        r'\byou should\s+(?:undergo|have|get|consider)\s+(?:surgery|treatment|therapy)',
        r'\btreatment options include\b',
        r'\bI recommend\s+(?:surgery|treatment|therapy|procedure)',
        r'\bconsider\s+(?:surgery|chemotherapy|radiation|transplant)',
    ]

    # Allowed disclaimer patterns
    REQUIRED_DISCLAIMERS = [
        "For Healthcare Professional use only",
        "Not a diagnostic tool",
        "Consult your healthcare provider",
        "This is not medical advice",
    ]

    def __init__(self):
        """Initialize the safety validator."""
        self._compile_patterns()

    def _compile_patterns(self):
        """Pre-compile regex patterns."""
        self.diagnostic_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.DIAGNOSTIC_PATTERNS
        ]
        self.prescriptive_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.PRESCRIPTIVE_PATTERNS
        ]
        self.prognosis_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.PROGNOSIS_PATTERNS
        ]
        self.treatment_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.TREATMENT_PATTERNS
        ]

    def check_diagnostic_language(self, text: str) -> dict[str, Any]:
        """Check for diagnostic language."""
        violations = []
        for pattern in self.diagnostic_patterns:
            matches = pattern.findall(text)
            if matches:
                violations.extend(matches)
        
        return {
            "category": "diagnostic",
            "is_safe": len(violations) == 0,
            "violations": violations,
        }

    def check_prescriptive_language(self, text: str) -> dict[str, Any]:
        """Check for prescriptive language."""
        violations = []
        for pattern in self.prescriptive_patterns:
            matches = pattern.findall(text)
            if matches:
                violations.extend(matches)
        
        return {
            "category": "prescriptive",
            "is_safe": len(violations) == 0,
            "violations": violations,
        }

    def check_prognosis_language(self, text: str) -> dict[str, Any]:
        """Check for prognosis language."""
        violations = []
        for pattern in self.prognosis_patterns:
            matches = pattern.findall(text)
            if matches:
                violations.extend(matches)
        
        return {
            "category": "prognosis",
            "is_safe": len(violations) == 0,
            "violations": violations,
        }

    def check_treatment_language(self, text: str) -> dict[str, Any]:
        """Check for treatment recommendation language."""
        violations = []
        for pattern in self.treatment_patterns:
            matches = pattern.findall(text)
            if matches:
                violations.extend(matches)
        
        return {
            "category": "treatment",
            "is_safe": len(violations) == 0,
            "violations": violations,
        }

    def validate_output(self, clinical_term: str, rationale: str) -> dict[str, Any]:
        """
        Validate a complete output for safety compliance.
        
        Returns safety assessment with sanitized output if needed.
        """
        combined_text = f"{clinical_term} {rationale}"
        
        checks = [
            self.check_diagnostic_language(combined_text),
            self.check_prescriptive_language(combined_text),
            self.check_prognosis_language(combined_text),
            self.check_treatment_language(combined_text),
        ]
        
        all_violations = []
        categories_violated = []
        
        for check in checks:
            if not check["is_safe"]:
                all_violations.extend(check["violations"])
                categories_violated.append(check["category"])
        
        is_safe = len(all_violations) == 0
        
        result = {
            "is_safe": is_safe,
            "categories_violated": categories_violated,
            "violation_count": len(all_violations),
            "reason": None,
            "sanitized_output": clinical_term,
        }
        
        if not is_safe:
            result["reason"] = f"Output contains {', '.join(categories_violated)} language"
            result["sanitized_output"] = self._sanitize_output(clinical_term)
        
        return result

    def _sanitize_output(self, text: str) -> str:
        """
        Sanitize output by removing unsafe language.
        
        Converts diagnostic statements to symptom descriptions.
        """
        sanitized = text
        
        # Replace "you have X" with "symptoms consistent with X"
        sanitized = re.sub(
            r'\byou have\s+',
            'symptoms consistent with ',
            sanitized,
            flags=re.IGNORECASE
        )
        
        # Replace "diagnosis" with "clinical interpretation"
        sanitized = re.sub(
            r'\bdiagnosis\b',
            'clinical interpretation',
            sanitized,
            flags=re.IGNORECASE
        )
        
        # Replace "treatment" with "management options"
        sanitized = re.sub(
            r'\btreatment\b',
            'management options',
            sanitized,
            flags=re.IGNORECASE
        )
        
        return sanitized

    def add_required_disclaimer(self, text: str) -> str:
        """Add required compliance disclaimer to output."""
        disclaimer = (
            "\n\n---\n"
            "⚠️ IMPORTANT: This is for Healthcare Professional use only. "
            "This system provides clinical terminology mapping, not medical diagnosis. "
            "Always consult qualified healthcare providers for medical decisions."
        )
        return text + disclaimer

    def validate_fair_balance(self, benefits: list[str], risks: list[str]) -> dict[str, Any]:
        """
        Validate Fair Balance compliance for drug information.
        
        Benefits and risks must be roughly equal in prominence.
        """
        benefit_word_count = sum(len(b.split()) for b in benefits)
        risk_word_count = sum(len(r.split()) for r in risks)
        
        # Fair Balance requires risks to have at least 70% of benefit word count
        balance_ratio = risk_word_count / max(benefit_word_count, 1)
        
        is_balanced = balance_ratio >= 0.7
        
        return {
            "is_balanced": is_balanced,
            "balance_ratio": balance_ratio,
            "benefit_word_count": benefit_word_count,
            "risk_word_count": risk_word_count,
            "recommendation": (
                None if is_balanced 
                else "Increase risk/safety information to meet Fair Balance requirements"
            ),
        }


# Singleton instance
safety_validator = SafetyValidator()
