"""
tests/test_prompt.py — Unit tests for the LLM prompt builder.
"""
import sys
import os
import pytest
import pandas as pd

# Ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from llm.prompt_builder import build_system_prompt, build_user_prompt, build_prompt, _dataframe_to_table

@pytest.fixture
def candidates_df():
    return pd.DataFrame({
        "restaurant_name": ["Pizza Paradise", "Burger King"],
        "cuisines": ["Italian", "American"],
        "aggregate_rating": [4.5, 3.8],
        "votes": [100, 200],
        "cost_for_two": [800, 400],
        "city": ["Delhi", "Mumbai"]
    })

@pytest.fixture
def preferences():
    return {
        "city": "Delhi",
        "budget": "low",
        "cuisines": ["Italian", "American"],
        "min_rating": 4.0,
        "additional_preferences": "Must have outdoor seating"
    }

def test_build_system_prompt():
    system_prompt = build_system_prompt()
    assert "expert restaurant recommendation assistant" in system_prompt
    assert "JSON array" in system_prompt

def test_dataframe_to_table(candidates_df):
    table = _dataframe_to_table(candidates_df)
    assert "Pizza Paradise" in table
    assert "Burger King" in table
    assert "₹800" in table
    assert "₹400" in table

def test_dataframe_to_table_empty():
    df = pd.DataFrame()
    table = _dataframe_to_table(df)
    assert "No restaurants found" in table

def test_build_user_prompt(candidates_df, preferences):
    user_prompt = build_user_prompt(candidates_df, preferences)
    assert "Location: Delhi" in user_prompt
    assert "Budget: low" in user_prompt
    assert "Italian, American" in user_prompt
    assert "4.0" in user_prompt
    assert "Must have outdoor seating" in user_prompt
    assert "Pizza Paradise" in user_prompt

def test_build_user_prompt_string_cuisines(candidates_df, preferences):
    prefs = preferences.copy()
    prefs["cuisines"] = "Italian"
    user_prompt = build_user_prompt(candidates_df, prefs)
    assert "Italian" in user_prompt

def test_build_prompt(candidates_df, preferences):
    sys_prompt, user_prompt = build_prompt(candidates_df, preferences)
    assert "expert restaurant recommendation assistant" in sys_prompt
    assert "Location: Delhi" in user_prompt
