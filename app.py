import streamlit as st

from machining_calc import calculate_feeds_speeds, generate_gcode, safety_check
from llm_parser import parse_user_request

st.set_page_config(page_title="AI CAM Advisor", page_icon="🛠️")

st.title("🛠️ AI CAM Advisor")
st.caption(
    "LLM samajhta hai kya karna hai — RPM/feed rate hamesha deterministic "
    "calculator se aata hai, LLM se nahi."
)

api_key = st.text_input("Anthropic API Key", type="password")

user_input = st.text_input(
    "Kya machine karna hai?",
    placeholder="e.g. aluminum mein 8mm hole drill karna hai, 12mm depth",
)

if st.button("Generate", type="primary"):
    if not api_key:
        st.error("API key daalo pehle.")
    elif not user_input:
        st.error("Kuch input to likho.")
    else:
        try:
            with st.spinner("LLM se request samajh rahe hain..."):
                parsed = parse_user_request(user_input, api_key=api_key)

            st.subheader("1. LLM ne ye samjha")
            st.json(parsed)

            params = calculate_feeds_speeds(
                material=parsed["material"],
                tool_diameter_mm=float(parsed["tool_diameter_mm"]),
            )

            st.subheader("2. Calculator ne ye nikala (deterministic, verified math)")
            st.json(params)

            warnings = safety_check(params)
            if warnings:
                st.subheader("⚠️ Safety Warnings")
                for w in warnings:
                    st.warning(w)

            gcode = generate_gcode(params, hole_depth_mm=float(parsed.get("hole_depth_mm", 10)))

            st.subheader("3. Generated G-code")
            st.code(gcode, language="gcode")

            st.error(
                "🚫 Yeh sirf ek draft hai. Machine par run karne se pehle "
                "ek qualified operator zaroor verify kare (dry run / simulator me test karo)."
            )

        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
st.caption(
    "Currently supported materials: aluminum, mild_steel, stainless_steel · "
    "Operation: drilling only (MVP scope)"
)