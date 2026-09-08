# 🛠️ AI CAM Advisor

An AI-assisted machining parameter advisor that turns plain-language requests into feeds, speeds, and G-code — while keeping every actual number deterministic and verifiable.

## The Idea

Large language models are great at understanding *intent* but weak at precise numeric computation — a well-known limitation when it comes to safety-critical outputs like CNC machining parameters.

This project demonstrates a safer design pattern:

> **LLM parses intent → Deterministic calculator computes numbers → Human verifies before running on a machine.**

The language layer never invents an RPM or feed rate. It only extracts structured data (material, tool diameter, depth) from natural language. All actual math — spindle speed, feed rate, chip load — runs through a fixed, auditable Python calculator using standard machining formulas.

## How It Works

1. **User input** (Hindi/English, casual phrasing): *"aluminum mein 8mm hole drill karna hai, 12mm depth"*
2. **Parser** extracts: `{material: aluminum, tool_diameter_mm: 8, hole_depth_mm: 12}`
3. **Calculator** computes RPM and feed rate using standard SFM/chip-load formulas
4. **Safety check** flags unusually high RPM, feed rate, or fragile tool diameters
5. **G-code generator** outputs a basic drilling cycle — clearly marked as a draft for human review

## Project Structure
├── app.py # Streamlit UI tying everything together
├── machining_calc.py # Deterministic feeds/speeds formulas + G-code template (source of truth)
├── llm_parser.py # Natural language -> structured JSON parser
└── requirements.txt # Dependencies

> **Note:** The current parser (`llm_parser.py`) uses keyword + regex matching as a lightweight stand-in for a real LLM call, so the demo runs without needing API credits. The architecture is designed so a real LLM (e.g. Claude via the Anthropic API) can be swapped in without touching `app.py` or the calculator — just replace the body of `parse_user_request()`.

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## Current Scope (MVP)

- **Materials:** aluminum, mild steel, stainless steel
- **Operation:** drilling
- **Output:** RPM, feed rate, safety warnings, draft G-code

## Next Steps

- Add facing/pocketing operations
- Swap in a real LLM call for more flexible language understanding
- Validate output against a G-code simulator (e.g. CAMotics) before display
- Expand the tool/material database (coatings, carbide vs HSS, tool deflection corrections)

## Disclaimer

This is a proof-of-concept / learning project. Output is **not** verified for real machining use — always have a qualified operator review parameters and dry-run any G-code before running it on an actual machine.
