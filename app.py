from urllib import response
import streamlit as st
import json
from main_llm import ask_openai
from fpdf import FPDF
from PIL import UnidentifiedImageError
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

st.set_page_config(page_title="Medical Equipment Assistant")
st.title("Medical Equipment Usage Assistant")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Load devices
with open("devices_data.json") as f:
    devices = json.load(f)

# Function to convert LLM response to PDF

def export_as_pdf(content, filename="instructions.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    text = c.beginText(40, 800)
    text.setFont("Helvetica", 12)

    for line in content.split('\n'):
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()
    return filename


# Device selection
device_names = [d["device_name"] for d in devices]
selected = st.selectbox("Select a medical device", device_names)

languages = ["English", "Hindi"]
selected_lang = st.selectbox("Select Language for Instructions", languages)


# Get selected device data
device = next(d for d in devices if d["device_name"] == selected)

# Create 2 columns: Left (info), Right (image)
left_col, right_col = st.columns([2, 1])

# Left: Device Info
with left_col:
    st.markdown("### 🩺 Device Overview")
    st.info(device["description"])

    st.markdown("### Usage Steps")
    for i, step in enumerate(device["usage"], start=1):
        st.markdown(f"- **Step {i}:** {step}")

    st.markdown("### Helpful Tip")
    st.warning(device["tips"])

# Right: Show Image
with right_col:
    image_path = os.path.join("images", device.get("image", ""))
    st.text(f"Looking for: {image_path}")
    st.text(f"Exists: {os.path.exists(image_path)}")

    try:
        if os.path.exists(image_path):
            st.image(image_path, caption=device["device_name"], use_container_width=True)
        else:
            st.warning("Image not available for this device.")
    except UnidentifiedImageError:
        st.error("Image file exists but is unreadable or corrupted.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

# Generate Instructions with LLM
if st.button("Generate LLM-Based Instructions", key="generate_btn"):
    prompt = f"""
    You are a helpful assistant.
    Explain in simple terms how to use the following medical device.

    Device: {device['device_name']}
    Description: {device['description']}
    Steps: {', '.join(device['usage'])}
    Tips: {device['tips']}
    """

    if selected_lang == "Hindi":
         prompt += "\n\nअब कृपया उपरोक्त जानकारी को सीधे हिंदी में सरल भाषा में समझाएं।"

    response = ask_openai(prompt)

    st.markdown("### Generated Instructions")
    st.success(response)


    # Download as .txt
    st.download_button(
        label="Download as .txt",
        data=response,
        file_name=f"{device['device_name'].lower().replace(' ', '_')}_instructions.txt",
        mime="text/plain"
    )

    # Download as PDF
    pdf_file_name = f"{device['device_name'].lower().replace(' ', '_')}_instructions.pdf"
    pdf_path = export_as_pdf(response, pdf_file_name)

    with open(pdf_path, "rb") as f:
        st.download_button(
            label="Download as PDF",
            data=f,
            file_name=pdf_file_name,
            mime="application/pdf"
        )

    os.remove(pdf_path)

# Ask Anything Section (only after generation)
    st.markdown("### Ask Anything About This Device")
    user_input = st.text_input("Ask a question about the selected device", placeholder="e.g. How do I clean this device?", key="chat_input")

    if st.button("Send Question", key="chat_send_btn"):
        if user_input:
            chat_prompt = f"""You are a medical assistant.
You are helping a user understand this device: {device['device_name']}
Device description: {device['description']}
Steps: {', '.join(device['usage'])}
Tips: {device['tips']}

Now answer the user's question:
Q: {user_input}
A:"""
            reply = ask_openai(chat_prompt)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Assistant", reply))

    for sender, message in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**You:** {message}")
        else:
            st.markdown(f"** Assistant:** {message}")
