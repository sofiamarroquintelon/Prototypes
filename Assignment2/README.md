# Cruz Verde Pharmacy Assistant

A smart Streamlit prototype built for the *Prototyping Products* course at ESADE as part of the MIBA program.  
This app helps users find medication recommendations based on their symptoms by combining LLMs (Cohere) with real pharmacy product data.

---

## About the Project

- **Concept:** Go beyond a basic prompt-response system by integrating a language model with real-world constraints like product availability, pricing, and branding.
- **Why this project?** I wanted to create a prototype that simulates a real assistant in a Guatemalan pharmacy (Cruz Verde), helping users identify the right medication and place an order easily.

---

## Utility

The app allows users to:

- Enter symptoms, age, weight, and gender  
- Get relevant medication suggestions via LLM (Cohere)  
- Match suggested medications with a local dataset (name, use, brand, and price)  
- View product info (image, price, manufacturer) and simulate a WhatsApp order  

This prototype shows how LLMs can enable intelligent assistance while remaining grounded in real data and product availability.

---

## Challenges & LLM Integration

- Making the use of the LLM *non-straightforward* was one of the main goals.
  - The system uses Cohere to interpret user symptoms, and then filters and matches the results with a structured product dataset to simulate realistic pharmacy interactions.
  - Although the LLM call itself is relatively direct, the value comes from post-processing its output, ensuring it's compatible with available medications, and presenting it in a user-friendly way.
- A secondary goal was to integrate an image recognizer that could identify medications from a photo (e.g., pill boxes), but this feature was not fully implemented.
  - Traditional OCR approaches were tested but proved unreliable.
  - A vision + LLM pipeline was planned but not completed.

---

## Tech Stack

- **Streamlit**
- **Cohere API**
- **Pandas**
- **Plotly** (for optional visualizations)
- **WhatsApp Web URL API** (simulated order flow)
- **python-dotenv**

---


