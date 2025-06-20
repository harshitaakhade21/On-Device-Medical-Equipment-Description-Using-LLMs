# On-Device-Medical-Equipment-Description-Using-LLMs

This project provides a user-friendly interface to generate real-time, natural language instructions for using medical devices. By integrating Large Language Models (LLMs), it helps healthcare workers and non-expert users understand complex medical equipment more easily — even in high-stress environments.

## Project Description

Medical equipment is often used in emergency or critical settings where quick understanding is crucial. This application uses LLMs to automatically describe how to use various medical devices and answer related questions in real time.

The app supports:
- Step-by-step instructions for each device
- Multi-language support (English, Hindi)
- Device image previews
- Interactive question-answering assistant
- PDF and text export of generated instructions


## Demo

![App Demo Screenshot] Are in images folder

## Features

- **Device Selection:** Choose from a list of medical devices
- **LLM Integration:** Generates natural language usage instructions
- **Language Switcher:** Instructions available in Hindi and English
- **Chat Mode:** Ask any question related to the selected device
- **Downloadable Outputs:** Get responses as `.txt` or `.pdf`
- **Image Previews:** Visual reference for each device


## Tech Stack

- [Streamlit](https://streamlit.io/) – Frontend UI
- [OpenAI API / Ollama](https://ollama.com) – LLM backend
- [FPDF](https://pyfpdf.readthedocs.io/) – PDF generation
- [Python](https://python.org) – Core logic
- `devices_data.json` – Structured device information


