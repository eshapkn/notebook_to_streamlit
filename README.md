# notebook_to_streamlit

A Streamlit app that helps Rosa choose a profitable promised delivery time from the notebook's simulated delivery model.

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The `rosa-starter` package is installed from GitHub as a read-only dependency. This project does not modify that repository.

## Run

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit in your browser.

## How to use

Choose a zone and time block, set the range of promise times, and adjust the margin, churn estimate, and refund cost. Click **Find best promised time** to compare the simulated net profit for each candidate.

## Streamlit Community Cloud

Push this project to its own GitHub repository, then create a new Streamlit Community Cloud app using `app.py` as the entry point. Streamlit Cloud will install the dependencies from `requirements.txt`.
