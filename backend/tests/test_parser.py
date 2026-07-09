"""
tests/test_parser.py — Unit tests for the LLM response parser.
"""
import sys
import os
import pytest
import json

# Ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from llm.parser import parse_recommendations, extract_json_from_text, validate_recommendation

def test_extract_json_from_text_bare_json():
    text = '[{"rank": 1, "restaurant_name": "Test", "explanation": "Good"}]'
    extracted = extract_json_from_text(text)
    assert extracted == text

def test_extract_json_from_text_markdown_fenced():
    text = "Here are your recommendations:\n```json\n[{\"rank\": 1, \"restaurant_name\": \"Test\", \"explanation\": \"Good\"}]\n```\nEnjoy!"
    extracted = extract_json_from_text(text)
    assert "rank" in extracted
    assert "```" not in extracted

def test_validate_recommendation_valid():
    rec = {"rank": 1, "restaurant_name": "Test", "explanation": "Good", "extra": 123}
    assert validate_recommendation(rec) == True

def test_validate_recommendation_missing_fields():
    rec1 = {"rank": 1, "restaurant_name": "Test"} # missing explanation
    rec2 = {"restaurant_name": "Test", "explanation": "Good"} # missing rank
    assert validate_recommendation(rec1) == False
    assert validate_recommendation(rec2) == False

def test_parse_recommendations_clean_json():
    text = '[{"rank": 1, "restaurant_name": "Test", "explanation": "Good"}]'
    recs = parse_recommendations(text)
    assert len(recs) == 1
    assert recs[0]["restaurant_name"] == "Test"

def test_parse_recommendations_fenced_json():
    text = "```\n[{\"rank\": 1, \"restaurant_name\": \"Test2\", \"explanation\": \"Nice\"}]\n```"
    recs = parse_recommendations(text)
    assert len(recs) == 1
    assert recs[0]["restaurant_name"] == "Test2"

def test_parse_recommendations_invalid_json():
    text = "This is not json at all."
    recs = parse_recommendations(text)
    assert len(recs) == 0

def test_parse_recommendations_skips_invalid_recs():
    # One valid, one invalid
    text = '[{"rank": 1, "restaurant_name": "Test", "explanation": "Good"}, {"rank": 2, "explanation": "Missing name"}]'
    recs = parse_recommendations(text)
    assert len(recs) == 1
    assert recs[0]["rank"] == 1
    
def test_parse_recommendations_sorts_by_rank():
    text = '[{"rank": 2, "restaurant_name": "Second", "explanation": "OK"}, {"rank": 1, "restaurant_name": "First", "explanation": "Best"}]'
    recs = parse_recommendations(text)
    assert len(recs) == 2
    assert recs[0]["rank"] == 1
    assert recs[1]["rank"] == 2
