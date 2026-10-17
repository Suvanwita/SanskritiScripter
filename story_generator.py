"""
story_generator.py — SanskritiScripter
Handles cultural data loading, prompt engineering, and Ollama-based story generation.
"""

import json
import os
import re
import requests
from typing import Optional

# ─────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────

DATA_FILE = os.path.join(os.path.dirname(__file__), "cultural_data.json")

# Model — override via OLLAMA_MODEL environment variable
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")

# Ollama base URL — override via OLLAMA_HOST environment variable
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

# Generation timeout in seconds
OLLAMA_TIMEOUT = int(os.environ.get("OLLAMA_TIMEOUT", "180"))


# ─────────────────────────────────────────────────────────────
# Data loading helpers
# ─────────────────────────────────────────────────────────────

def load_cultural_data() -> dict:
    """Load cultural data from JSON file."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_regions() -> list[str]:
    return load_cultural_data()["regions"]


def get_languages() -> list[str]:
    return load_cultural_data()["languages"]


def get_festivals() -> list[str]:
    return load_cultural_data()["festivals"]


def get_morals() -> list[str]:
    return load_cultural_data()["morals"]


def get_cultural_context(region: str, festival: str) -> dict:
    """
    Return structured cultural grounding information for a given region + festival.
    Falls back gracefully if the combination is not in the data.
    """
    data = load_cultural_data()
    ctx = data.get("cultural_context", {})

    region_ctx = ctx.get(region, {})
    festival_ctx = region_ctx.get(festival, {})

    if festival_ctx:
        return festival_ctx

    # Try to find the festival under any region (cross-region fallback)
    for r, festivals in ctx.items():
        if festival in festivals:
            return festivals[festival]

    # Last resort: return festival_info summary
    info = data.get("festival_info", {}).get(festival, {})
    if info:
        return {
            "summary": info.get("description", f"{festival} is celebrated with joy and community."),
            "elements": [],
            "atmosphere": "festive and joyful",
            "typical_characters": [],
            "story_hooks": [],
        }

    return {
        "summary": f"{festival} is a vibrant Indian festival celebrated with community gatherings.",
        "elements": [],
        "atmosphere": "festive",
        "typical_characters": [],
        "story_hooks": [],
    }


# ─────────────────────────────────────────────────────────────
# Age-based vocabulary guidance
# ─────────────────────────────────────────────────────────────

def get_age_guidance(age: int) -> str:
    if age <= 7:
        return (
            "Use very simple, short sentences. Vocabulary should be suitable for a 5–7 year old. "
            "Use concrete images, repetition, and gentle wonder. Sentences should be short (under 15 words). "
            "Avoid complex metaphors. Use lots of dialogue and action."
        )
    elif age <= 10:
        return (
            "Use clear, engaging prose for an 8–10 year old. Moderate vocabulary — introduce one or two new "
            "cultural words but explain them naturally in context. Include dialogue, description and mild tension. "
            "Sentences can be varied in length."
        )
    else:
        return (
            "Use richer, more descriptive storytelling for an 11–13 year old. Include sensory detail, "
            "internal reflection, and more nuanced cultural description. Vocabulary can be more sophisticated. "
            "The conflict should feel meaningful and the resolution emotionally satisfying."
        )


# ─────────────────────────────────────────────────────────────
# Prompt builder
# ─────────────────────────────────────────────────────────────

def create_story_prompt(
    child_name: str,
    child_age: int,
    region: str,
    festival: str,
    language: str,
    story_idea: str,
    moral: str,
    cultural_context: dict,
) -> str:
    """Build the story-generation prompt sent to Ollama."""

    age_guidance = get_age_guidance(child_age)

    elements_text = ""
    if cultural_context.get("elements"):
        elements_list = "\n".join(f"  - {e}" for e in cultural_context["elements"])
        elements_text = f"\nAuthentic cultural elements to weave into the story naturally:\n{elements_list}"

    hooks_text = ""
    if cultural_context.get("story_hooks") and not story_idea.strip():
        hooks_text = (
            f"\nSuggested story directions (choose or blend):\n"
            + "\n".join(f"  - {h}" for h in cultural_context["story_hooks"][:3])
        )

    idea_text = f"\nThe person requesting the story suggested this idea: {story_idea.strip()}" if story_idea.strip() else ""

    regional_language_note = ""
    if language != "English":
        regional_language_note = (
            f"\nIMPORTANT: The 'regional_text' field of EVERY chapter MUST be written in {language}. "
            f"This is not a translation note — produce actual {language} prose. "
            f"If you are not confident writing full {language}, produce your best effort. "
            f"The 'english_text' must always be in English."
        )
    else:
        regional_language_note = (
            "\nFor the 'regional_text' field, write the text in Bengali (বাংলা) as the default regional language."
        )

    prompt = f"""You are a master storyteller specialising in children's literature rooted in Indian culture.

TASK: Write an original children's story with ALL of the following requirements.

═══ STORY REQUIREMENTS ═══
- Hero/protagonist: a child named {child_name}, aged {child_age}
- Setting: {region}, India, during {festival}
- Story moral / central value: {moral}
- Festival / cultural context: {cultural_context.get("summary", festival)}
- Atmosphere: {cultural_context.get("atmosphere", "festive and warm")}
{idea_text}

═══ AGE-APPROPRIATE WRITING ═══
{age_guidance}

═══ CULTURAL AUTHENTICITY ═══
{elements_text}
- Weave cultural elements into the story naturally — do NOT list them.
- Do NOT invent cultural facts. Use only elements appropriate to {festival} in {region}.
- Show the culture through character actions, dialogue, and sensory detail.
- Avoid cultural stereotypes. Show community, warmth and dignity.
{hooks_text}

═══ STORY STRUCTURE ═══
- Exactly 4 chapters
- Each chapter should be 3–5 paragraphs (substantial, not just a few lines)
- Include meaningful dialogue in every chapter
- Create a clear conflict (problem/challenge) by Chapter 2
- Resolve the conflict positively by Chapter 4
- End with the moral expressed naturally through the story — not as a lecture
- Give the story a compelling, culturally resonant title
- Include 2–4 named characters (besides {child_name})

═══ OUTPUT FORMAT ═══
{regional_language_note}

You MUST respond with ONLY a valid JSON object. Do not include any text before or after the JSON.
Do not wrap the JSON in markdown code blocks. Output raw JSON only.

The JSON must follow this exact schema:
{{
  "title": "Story title here",
  "characters": ["Character 1", "Character 2", "Character 3"],
  "moral": "The moral of the story",
  "chapters": [
    {{
      "chapter_number": 1,
      "title": "Chapter title",
      "english_text": "Full chapter text in English (3–5 paragraphs with dialogue)",
      "regional_text": "Full chapter text in {language if language != 'English' else 'Bengali'} (3–5 paragraphs)",
      "scene_description": "A single evocative sentence describing the key visual scene of this chapter, suitable as an illustration prompt"
    }},
    {{
      "chapter_number": 2,
      "title": "Chapter title",
      "english_text": "...",
      "regional_text": "...",
      "scene_description": "..."
    }},
    {{
      "chapter_number": 3,
      "title": "Chapter title",
      "english_text": "...",
      "regional_text": "...",
      "scene_description": "..."
    }},
    {{
      "chapter_number": 4,
      "title": "Chapter title",
      "english_text": "...",
      "regional_text": "...",
      "scene_description": "..."
    }}
  ]
}}

Remember: output ONLY the JSON. No preamble, no explanation, no markdown fences."""

    return prompt


# ─────────────────────────────────────────────────────────────
# Ollama connectivity
# ─────────────────────────────────────────────────────────────

def check_ollama_available() -> tuple[bool, str]:
    """
    Returns (is_available: bool, message: str).
    Checks if the Ollama server is reachable.
    """
    try:
        resp = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if resp.status_code == 200:
            return True, "Ollama is running."
        return False, f"Ollama responded with status {resp.status_code}."
    except requests.exceptions.ConnectionError:
        return False, (
            f"Cannot connect to Ollama at {OLLAMA_HOST}. "
            "Please start Ollama: run `ollama serve` in a terminal."
        )
    except requests.exceptions.Timeout:
        return False, "Ollama connection timed out."
    except Exception as e:
        return False, f"Unexpected error checking Ollama: {e}"


def check_model_available(model: str) -> tuple[bool, str]:
    """Check whether a specific model is pulled locally."""
    try:
        resp = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if resp.status_code != 200:
            return False, "Could not list Ollama models."
        models = [m.get("name", "") for m in resp.json().get("models", [])]
        # Match base name (e.g. "qwen2.5:7b" matches "qwen2.5:7b" or "qwen2.5")
        base = model.split(":")[0]
        for m in models:
            if m == model or m.startswith(base):
                return True, f"Model '{model}' is available."
        return False, (
            f"Model '{model}' is not installed. "
            f"Run: `ollama pull {model}` to download it."
        )
    except Exception as e:
        return False, f"Could not verify model: {e}"


# ─────────────────────────────────────────────────────────────
# JSON parsing — robust
# ─────────────────────────────────────────────────────────────

def _extract_json(text: str) -> Optional[str]:
    """Try to extract a JSON object from raw LLM output."""
    # Direct parse first
    text = text.strip()
    try:
        json.loads(text)
        return text
    except json.JSONDecodeError:
        pass

    # Strip markdown fences
    fenced = re.sub(r"```(?:json)?\s*", "", text)
    fenced = fenced.replace("```", "").strip()
    try:
        json.loads(fenced)
        return fenced
    except json.JSONDecodeError:
        pass

    # Find first { ... } block
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start : end + 1]
        try:
            json.loads(candidate)
            return candidate
        except json.JSONDecodeError:
            pass

    return None


def parse_story_response(raw: str) -> tuple[Optional[dict], Optional[str]]:
    """
    Parse the LLM response into a story dict.
    Returns (story_dict, error_message).
    On success: (dict, None). On failure: (None, error_str).
    """
    extracted = _extract_json(raw)
    if extracted is None:
        snippet = raw[:400].replace("\n", " ")
        return None, (
            f"The AI response did not contain valid JSON.\n\n"
            f"Raw output preview:\n```\n{snippet}…\n```\n\n"
            "Try regenerating — the model sometimes produces malformed output on the first attempt."
        )

    try:
        story = json.loads(extracted)
    except json.JSONDecodeError as e:
        return None, f"JSON parsing failed: {e}\n\nTry regenerating the story."

    # Validate required fields
    required_top = ["title", "chapters", "moral"]
    for field in required_top:
        if field not in story:
            return None, f"Story is missing required field: '{field}'. Try regenerating."

    chapters = story.get("chapters", [])
    if not isinstance(chapters, list) or len(chapters) == 0:
        return None, "Story has no chapters. Try regenerating."

    # Normalise chapter fields — fill in missing keys gracefully
    for i, ch in enumerate(chapters):
        ch.setdefault("chapter_number", i + 1)
        ch.setdefault("title", f"Chapter {i + 1}")
        ch.setdefault("english_text", ch.get("text_en", ch.get("text", "")))
        ch.setdefault("regional_text", ch.get("text_regional", ch.get("regional_text", ch.get("english_text", ""))))
        ch.setdefault("scene_description", ch.get("illustration_desc", "A scene from the story"))

    story.setdefault("characters", [])
    return story, None


# ─────────────────────────────────────────────────────────────
# Ollama call
# ─────────────────────────────────────────────────────────────

def call_ollama(prompt: str, model: str) -> tuple[Optional[str], Optional[str]]:
    """
    Send the prompt to Ollama and return (raw_text, error).
    Uses the /api/generate endpoint with stream=False.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.85,
            "top_p": 0.92,
            "num_predict": 4096,
        },
    }
    try:
        resp = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json=payload,
            timeout=OLLAMA_TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        raw = data.get("response", "")
        if not raw:
            return None, "Ollama returned an empty response. Try a different model or regenerate."
        return raw, None
    except requests.exceptions.ConnectionError:
        return None, (
            "Lost connection to Ollama during generation. "
            "Please ensure `ollama serve` is still running."
        )
    except requests.exceptions.Timeout:
        return None, (
            f"Ollama generation timed out after {OLLAMA_TIMEOUT}s. "
            "Try a smaller/faster model or increase OLLAMA_TIMEOUT."
        )
    except requests.exceptions.HTTPError as e:
        body = ""
        try:
            body = e.response.json().get("error", "")
        except Exception:
            pass
        msg = body or str(e)
        if "model" in msg.lower() and "not found" in msg.lower():
            return None, (
                f"Model '{model}' not found. "
                f"Run: `ollama pull {model}` to download it, then try again."
            )
        return None, f"Ollama HTTP error: {msg}"
    except Exception as e:
        return None, f"Unexpected error calling Ollama: {e}"


# ─────────────────────────────────────────────────────────────
# Main generation entry point
# ─────────────────────────────────────────────────────────────

def generate_story(
    child_name: str,
    child_age: int,
    region: str,
    festival: str,
    language: str,
    story_idea: str,
    moral: str,
    demo_mode: bool = False,
    model: Optional[str] = None,
) -> tuple[Optional[dict], Optional[str]]:
    """
    Generate a story.

    Args:
        demo_mode: If True, skip Ollama and return the built-in mock story.
        model:     Ollama model name to use (defaults to OLLAMA_MODEL env var).

    Returns:
        (story_dict, error_message)
        On success: (dict, None)
        On failure: (None, error_str)
    """
    if model is None:
        model = OLLAMA_MODEL

    # ── Demo mode ──────────────────────────────────────────
    if demo_mode:
        data = load_cultural_data()
        mock = data["mock_story"].copy()
        mock["requested_child_name"] = child_name
        mock["requested_age"] = child_age
        mock["requested_region"] = region
        mock["requested_festival"] = festival
        mock["requested_language"] = language
        mock["requested_idea"] = story_idea
        mock["requested_moral"] = moral
        mock["_demo"] = True
        return mock, None

    # ── Check Ollama is running ────────────────────────────
    available, avail_msg = check_ollama_available()
    if not available:
        return None, (
            "**Ollama is not available.** " + avail_msg + "\n\n"
            "Please start Ollama and ensure the selected model is installed.\n\n"
            "You can also switch to **Demo Mode** in the sidebar to preview the app without Ollama."
        )

    # ── Check model is installed ───────────────────────────
    model_ok, model_msg = check_model_available(model)
    if not model_ok:
        return None, f"**Model not ready.** {model_msg}"

    # ── Build cultural context and prompt ──────────────────
    cultural_context = get_cultural_context(region, festival)
    prompt = create_story_prompt(
        child_name=child_name,
        child_age=child_age,
        region=region,
        festival=festival,
        language=language,
        story_idea=story_idea,
        moral=moral,
        cultural_context=cultural_context,
    )

    # ── Call Ollama ────────────────────────────────────────
    raw, err = call_ollama(prompt, model)
    if err:
        return None, err

    # ── Parse response ─────────────────────────────────────
    story, parse_err = parse_story_response(raw)
    if parse_err:
        return None, parse_err

    # Attach request metadata
    story["requested_child_name"] = child_name
    story["requested_age"] = child_age
    story["requested_region"] = region
    story["requested_festival"] = festival
    story["requested_language"] = language
    story["requested_idea"] = story_idea
    story["requested_moral"] = moral
    story["_demo"] = False

    # Alias for display compatibility
    story.setdefault("region", region)
    story.setdefault("festival", festival)
    story.setdefault("language", language)

    return story, None
