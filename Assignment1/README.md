# Hotel Booking Insights

A Streamlit prototype developed for the *Prototyping Products* course at ESADE as part of the MIBA program.  
This app helps hotels explore and analyze their booking data interactively, supporting better, data-driven decisions.

---

## About the Project

- **Dataset Used:** `hotelbooking.csv` from the Cloud Computing course (2024 Term)
- **Why this project?** I wanted to create a tool that helps hotels visualize their data more effectively and identify patterns to reduce cancellations and improve customer retention.

---

## Utility

The app allows users to:

- Visualize reservations over time
- Identify trends in customer loyalty and guest origin
- Support decisions such as optimizing promotions during key holidays
- Detect patterns related to cancellations and booking channels

---

## Main Challenges

- Selecting the most relevant variables from the dataset
- Choosing which Streamlit features to include (there are so many)
- Some features like `st.tags` and calendar heatmaps didn’t work as expected, so I had to find alternatives like `st.multiselect` and a standard calendar
- Learning how to properly implement the selected widgets — trial and error and a bit of help from ChatGPT made it work

---

## Tech Stack

- **Python**
- **Streamlit**
- **Pandas / Numpy**
- **scikit-learn** (for optional model use)
- **Plotly / Seaborn** for visualizations

---
