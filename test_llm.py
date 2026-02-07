#!/usr/bin/env python3
"""Test script to debug LLM response truncation"""

import sys
sys.path.insert(0, r'e:\Plaksha\Medithon 2026\Paeon-AI-main\Paeon-AI-main')

import json
import google.generativeai as genai
from backend.app.core.config import settings

# Configure Gemini
genai.configure(api_key=settings.gemini_api_key)
model = genai.GenerativeModel(settings.gemini_model)

print(f"Using API Key: {settings.gemini_api_key[:20]}...")
print(f"Using Model: {settings.gemini_model}")
print()

# Test 1: Simple text
print("=" * 60)
print("TEST 1: Simple text generation")
print("=" * 60)
prompt1 = "Hello, who are you?"
response1 = model.generate_content(
    contents=prompt1,
    generation_config={
        "max_output_tokens": 100,
        "temperature": 0.0,
        "stream": False,
    }
)
print(f"Response type: {type(response1)}")
print(f"Response dir: {[x for x in dir(response1) if not x.startswith('_')]}")
print(f"response.text: {repr(response1.text)}")
print(f"response.text length: {len(response1.text)}")
if hasattr(response1, 'candidates'):
    print(f"response.candidates: {response1.candidates}")
    if response1.candidates:
        c = response1.candidates[0]
        print(f"  candidate[0] type: {type(c)}")
        print(f"  candidate[0] dir: {[x for x in dir(c) if not x.startswith('_')]}")
        if hasattr(c, 'content'):
            print(f"  candidate[0].content: {c.content}")
            print(f"  candidate[0].content.parts: {c.content.parts}")
            if c.content.parts:
                print(f"    parts[0]: {c.content.parts[0]}")
                print(f"    parts[0].text: {repr(c.content.parts[0].text)}")
print()

# Test 2: JSON generation
print("=" * 60)
print("TEST 2: JSON generation (the problematic one)")
print("=" * 60)
prompt2 = 'Map "my feet are burning" to clinical term. Return ONLY JSON: {"clinical_term": "term", "snomed_code": "code", "icd10_code": "code", "confidence": 0.7}'
response2 = model.generate_content(
    contents=prompt2,
    generation_config={
        "max_output_tokens": 200,
        "temperature": 0.0,
        "stream": False,
    }
)
print(f"Response type: {type(response2)}")
print(f"response.text: {repr(response2.text)}")
print(f"response.text length: {len(response2.text)}")
if hasattr(response2, 'candidates'):
    print(f"response.candidates: {response2.candidates}")
    if response2.candidates:
        c = response2.candidates[0]
        if hasattr(c, 'content'):
            print(f"  candidate[0].content: {c.content}")
            if c.content.parts:
                print(f"    parts[0]: {repr(c.content.parts[0])}")
                print(f"    parts[0].text: {repr(c.content.parts[0].text)}")
print()

# Test 3: With explicit format
print("=" * 60)
print("TEST 3: JSON with different format")
print("=" * 60)
prompt3 = f'''You are a clinical mapper. Return ONLY valid JSON.

Symptom: "burning feet"

Response format:
{{"clinical_term": "...", "snomed_code": "...", "icd10_code": "...", "confidence": 0.7}}'''

response3 = model.generate_content(
    contents=prompt3,
    generation_config={
        "max_output_tokens": 300,
        "temperature": 0.0,
        "stream": False,
    }
)
print(f"Response type: {type(response3)}")
print(f"response.text: {repr(response3.text)}")
print(f"response.text length: {len(response3.text)}")
print()

# Test 4: Check if usage/tokens info is available
print("=" * 60)
print("TEST 4: Response metadata")
print("=" * 60)
print(f"Response object attributes: {[x for x in dir(response3) if not x.startswith('_')]}")
