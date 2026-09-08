import re

from machining_calc import VALID_MATERIALS

MATERIAL_KEYWORDS = {
    "aluminum": "aluminum",
    "aluminium": "aluminum",
    "alu": "aluminum",
    "steel": "mild_steel",
    "mild steel": "mild_steel",
    "mild_steel": "mild_steel",
    "stainless": "stainless_steel",
    "stainless steel": "stainless_steel",
    "ss": "stainless_steel",
}


def parse_user_request(user_text, api_key=None):
    text = user_text.lower()
    material = None
    for keyword, mapped in MATERIAL_KEYWORDS.items():
        if keyword in text:
            material = mapped
            break
    if material is None:
        raise ValueError("Couldn't find a known material. Try: aluminum, steel, stainless steel")
    numbers = re.findall(r"\d+\.?\d*", text)
    numbers = [float(n) for n in numbers]
    if not numbers:
        raise ValueError("Couldn't find any numbers (tool diameter) in your text.")
    tool_diameter_mm = numbers[0]
    hole_depth_mm = numbers[1] if len(numbers) > 1 else 10
    if '"' in user_text or "inch" in text:
        tool_diameter_mm = tool_diameter_mm * 25.4
    operation = "facing" if "face" in text or "facing" in text else "drilling"
    return {
        "material": material,
        "tool_diameter_mm": tool_diameter_mm,
        "operation": operation,
        "hole_depth_mm": hole_depth_mm,
    }