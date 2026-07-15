# Pak Angels AI Tutor

Pak Angels AI Tutor is an accessible Streamlit learning platform for students,
faculty, professionals, entrepreneurs, and startup founders. It teaches AI from
foundations through practical application development and guides learners through
the **Idea → Design → Build → Test → Share** journey.

## Features

- Eleven specialized learning areas
- Context-aware AI tutor using the OpenAI Responses API
- Streaming answers and separate chat history for every learning area
- AI Application Builder questionnaire and project-prompt generator
- Demonstration mode that works without an API key
- Secure Streamlit Secrets configuration
- Responsive Pak Angels visual design
- GitHub and Streamlit Community Cloud-ready structure

The tested package versions are pinned in `requirements.txt` so Streamlit Cloud
builds the same dependency set used during verification.

## Project files

```text
.
├── app.py
├── tutor_config.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit
    ├── config.toml
    └── secrets.toml.example
```

## Run locally

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The application launches in demonstration mode when no API key is configured.

For live AI responses, create `.streamlit/secrets.toml` locally:

```toml
OPENAI_API_KEY = "your-api-key-here"
OPENAI_MODEL = "gpt-4.1-mini"
```

Never upload `.streamlit/secrets.toml` or an API key to GitHub.

## Deploy on Streamlit Community Cloud

1. Upload this project to a GitHub repository.
2. Sign in at <https://share.streamlit.io/> with GitHub.
3. Select **Create app** and choose the repository.
4. Choose the `main` branch and enter `app.py` as the entrypoint.
5. Open **Advanced settings** and paste the following into **Secrets**:

   ```toml
   OPENAI_API_KEY = "your-api-key-here"
   OPENAI_MODEL = "gpt-4.1-mini"
   ```

6. Click **Deploy**.

If you are not ready to use the OpenAI API, deploy without secrets. The full
interface and project-prompt generator will work in demonstration mode.

## Security and cost controls

- API credentials are read only from Streamlit Secrets or environment variables.
- ChatGPT subscriptions and OpenAI API billing are separate.
- Set a project budget and usage notification in the API platform before sharing
  the application widely.
- Chat history is kept only in the current Streamlit browser session. This version
  does not maintain student accounts or permanent personal records.
- Do not enter confidential, medical, financial, or personally identifying data.

## Updating the deployed application

Edit and commit a file in GitHub. Streamlit Community Cloud detects the commit and
automatically redeploys the application.
