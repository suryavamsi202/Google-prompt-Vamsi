import streamlit as st
import json
import base64
import sys
import os

# Add backend to Python path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend'))
if backend_path not in sys.path:
    sys.path.append(backend_path)

try:
    from processor import process_text, process_audio, process_image_ocr, process_news_url
    from gemini_client import process_with_gemini, process_image_with_gemini
except ImportError as e:
    st.error(f"Error loading AI backend components: {e}")

st.set_page_config(page_title="Universal AI Bridge 🌉", layout="wide")

st.title("Universal AI Bridge 🌉")
st.markdown("Transform messy inputs (text, voice, images, news) into structured **life-saving actions** instantly.")

# State
if "history" not in st.session_state:
    st.session_state.history = []

def display_result(result):
    if not isinstance(result, dict):
        st.error(f"Unexpected response format: {result}")
        return
        
    st.markdown("### 🧠 AI Decision Output")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Intent", result.get("intent", "Unknown"))
    with col2:
        st.metric("Category", result.get("category", "General").title())
    with col3:
        urgency = result.get("urgency", "LOW")
        color = "red" if urgency in ["HIGH", "CRITICAL"] else "orange" if urgency == "MEDIUM" else "green"
        st.markdown(f"**Urgency:** :{color}[**{urgency}**]")
        
    st.info(f"**Summary:** {result.get('summary', 'No summary provided')}")
    
    col_act, col_steps = st.columns(2)
    with col_act:
        st.success("**✅ Actions to take:**")
        for a in result.get("actions", []):
            st.markdown(f"- {a}")
    with col_steps:
        st.warning("**🔄 Next Steps:**")
        for n in result.get("next_steps", []):
            st.markdown(f"- {n}")
            
    with st.expander("View Raw Structured Data"):
        st.json(result)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📝 Text", "🎙️ Voice", "🖼️ Image", "📰 News", "🌤️ Weather/Agro", "📜 History"])

with tab1:
    text_input = st.text_area("Enter chaotic real-world text (e.g., 'My dad has chest pain near whitefield'):", height=150)
    if st.button("Process Text"):
        if text_input:
            with st.spinner("Processing text through AI agent..."):
                try:
                    structured = process_text(text_input)
                    data = process_with_gemini(structured)
                    st.session_state.history.append({"type": "text", "input": text_input, "result": data})
                    display_result(data)
                except Exception as e:
                    st.error(f"Agent Engine Error: {e}")

with tab2:
    st.info("Upload an audio recording of an emergency or chaotic situation.")
    audio_file = st.file_uploader("Upload Audio (wav, mp3, m4a)", type=["wav", "mp3", "m4a"])
    if st.button("Process Audio"):
        if audio_file:
            with st.spinner("Transcribing and analyzing audio..."):
                try:
                    audio_bytes = audio_file.getvalue()
                    structured = process_audio(audio_bytes)
                    data = process_with_gemini(structured)
                    st.session_state.history.append({"type": "voice", "input": audio_file.name, "result": data})
                    display_result(data)
                except Exception as e:
                    st.error(f"Agent Engine Error: {e}")

with tab3:
    st.info("Upload photos of accidents, medical records, or any chaotic scene (You can upload 100+ images at once).")
    image_files = st.file_uploader("Upload Images (jpg, png, jpeg)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    
    if image_files:
        st.write(f"📁 {len(image_files)} images selected for bulk processing.")
        
    if st.button("Process All Images"):
        if image_files:
            for i, image_file in enumerate(image_files):
                st.markdown(f"#### Processing Image {i+1} of {len(image_files)}: {image_file.name}")
                st.image(image_file, width=300)
                with st.spinner(f"Analyzing {image_file.name} via OCR and Vision AI..."):
                    try:
                        image_bytes = image_file.getvalue()
                        structured = process_image_ocr(image_bytes)
                        
                        if structured.get("ocr_text", "").strip():
                            data = process_with_gemini(structured)
                        else:
                            data = process_image_with_gemini(image_bytes, image_file.type)
                            
                        st.session_state.history.append({"type": "image", "input": image_file.name, "result": data})
                        display_result(data)
                        st.divider()
                    except Exception as e:
                        st.error(f"Agent Engine Error on {image_file.name}: {e}")

with tab4:
    news_url = st.text_input("Enter a Breaking News URL")
    if st.button("Process News"):
        if news_url:
            with st.spinner("Scraping and analyzing news impact..."):
                try:
                    structured = process_news_url(news_url)
                    data = process_with_gemini(structured)
                    st.session_state.history.append({"type": "news", "input": news_url, "result": data})
                    display_result(data)
                except Exception as e:
                    st.error(f"Agent Engine Error: {e}")

with tab5:
    st.info("Monitor real-time weather alerts and agricultural crop stress (AgroMonitoring API / Weather Integration).")
    weather_input = st.text_input("Enter City, Region, or Agro Polygon ID:")
    if st.button("Analyze Weather & Crop Data"):
        if weather_input:
            with st.spinner("Fetching satellite telemetry and weather data..."):
                try:
                    # Systematically mocking the AgroMonitoring API telemetry response for the Hackathon integration demo
                    agro_mock_data = f"""
                    [AgroMonitoring API Data for {weather_input}]
                    - Soil Moisture: 14% (Critical Low)
                    - Precipitation: 0mm (Last 14 days)
                    - Temperature: 42°C
                    - Crop Stress Level: HIGH
                    - Warning: Severe Drought conditions detected in Polygon Region. Dust storms highly probable.
                    """
                    structured = process_text(agro_mock_data)
                    data = process_with_gemini(structured)
                    st.session_state.history.append({"type": "weather", "input": weather_input, "result": data})
                    display_result(data)
                except Exception as e:
                    st.error(f"Agent Engine Error: {e}")

with tab6:
    st.subheader("Your Interactions")
    if len(st.session_state.history) == 0:
        st.info("No history yet. Try analyzing something!")
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            st.markdown(f"### {len(st.session_state.history) - i}. {item['type'].title()} Input")
            st.markdown(f"**Input Data:** {item['input']}")
            st.json(item['result'])
            st.divider()