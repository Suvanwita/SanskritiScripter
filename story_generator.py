"""
story_generator.py
Handles story generation logic. Currently returns mock story data.
In future iterations, this will call Ollama for AI generation.
"""

import json
import os
from typing import Optional


DATA_FILE = os.path.join(os.path.dirname(__file__), "cultural_data.json")


def load_cultural_data() -> dict:
    """Load cultural data from JSON file."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_regions() -> list[str]:
    data = load_cultural_data()
    return data["regions"]


def get_languages() -> list[str]:
    data = load_cultural_data()
    return data["languages"]


def get_festivals() -> list[str]:
    data = load_cultural_data()
    return data["festivals"]


def get_morals() -> list[str]:
    data = load_cultural_data()
    return data["morals"]


def generate_story(
    child_name: str,
    child_age: int,
    region: str,
    festival: str,
    language: str,
    story_idea: str,
    moral: str,
) -> Optional[dict]:
    """
    Generate a story based on the provided parameters.

    Currently returns mock story data.
    Future: call Ollama API to generate real personalized stories.
    """
    data = load_cultural_data()
    story = data["mock_story"].copy()

    # Personalise the mock story with user inputs where applicable
    story["requested_child_name"] = child_name
    story["requested_age"] = child_age
    story["requested_region"] = region
    story["requested_festival"] = festival
    story["requested_language"] = language
    story["requested_idea"] = story_idea
    story["requested_moral"] = moral

    # Note: In the real version, we would call Ollama here:
    # prompt = build_prompt(child_name, child_age, region, festival, language, story_idea, moral)
    # story = call_ollama(prompt)

    return story
