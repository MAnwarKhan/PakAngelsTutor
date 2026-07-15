"""Pak Angels AI Tutor — Streamlit Community Cloud application."""

from __future__ import annotations

import os
from typing import Iterator

import streamlit as st
from openai import OpenAI

from tutor_config import BUILDER_STEPS, MODULES, system_instructions


APP_NAME = "Pak Angels AI Tutor"
APP_TAGLINE = "Learn • Build • Innovate • Launch with Artificial Intelligence"
DEFAULT_MODEL = "gpt-4.1-mini"


st.set_page_config(
    page_title=APP_NAME,
    page_icon="🪽",
    layout="wide",
    initial_sidebar_state="expanded",
)


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root { --pa-blue:#0756a3; --pa-navy:#07305f; --pa-sky:#eaf4ff; --pa-gold:#f6b93b; }
        .stApp { background: linear-gradient(180deg,#f7fbff 0,#ffffff 30rem); }
        .block-container { max-width: 1120px; padding-top: 1.5rem; padding-bottom: 3rem; }
        [data-testid="stSidebar"] { background: linear-gradient(180deg,#062f5d,#0756a3); }
        [data-testid="stSidebar"] * { color: white; }
        [data-testid="stSidebar"] .stRadio label { padding:.18rem 0; }
        [data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.22); }
        .pa-hero { padding:2rem 2.2rem; border-radius:24px; color:white;
          background:linear-gradient(125deg,var(--pa-navy),var(--pa-blue));
          box-shadow:0 16px 38px rgba(7,48,95,.16); margin-bottom:1.2rem; }
        .pa-hero h1 { margin:0 0 .35rem; font-size:2.45rem; line-height:1.1; }
        .pa-hero p { margin:.25rem 0; color:#eaf4ff; font-size:1.05rem; }
        .pa-pill { display:inline-block; margin-top:.8rem; padding:.34rem .7rem;
          border-radius:999px; color:#07305f; background:#fff; font-weight:700; font-size:.82rem; }
        .pa-module { padding:1rem 1.1rem; background:white; border:1px solid #dbe9f7;
          border-radius:16px; min-height:116px; box-shadow:0 5px 18px rgba(7,48,95,.06); }
        .pa-module h3 { color:#07305f; font-size:1.08rem; margin:.1rem 0 .4rem; }
        .pa-module p { color:#42566b; font-size:.9rem; margin:0; }
        .pa-step { border-left:4px solid #0b72cf; padding:.45rem .8rem; margin:.25rem 0 .7rem;
          background:#f3f8fe; border-radius:0 10px 10px 0; }
        .pa-step strong { color:#07305f; }
        .pa-note { padding:.8rem 1rem; border-radius:12px; background:#fff8e7;
          border:1px solid #f5d58d; color:#644b12; }
        .stChatMessage { border:1px solid #e1ebf5; border-radius:16px; background:white; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def secret_value(name: str, default: str = "") -> str:
    """Read configuration from Streamlit secrets, then environment variables."""
    try:
        value = st.secrets.get(name, "")
    except (FileNotFoundError, KeyError):
        value = ""
    return str(value or os.getenv(name, default)).strip()


def initialize_state() -> None:
    defaults = {
        "messages": {},
        "learner_context": "",
        "builder_answers": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def current_messages(module_name: str) -> list[dict[str, str]]:
    return st.session_state.messages.setdefault(module_name, [])


def stream_response(
    client: OpenAI,
    model: str,
    module_name: str,
    messages: list[dict[str, str]],
) -> Iterator[str]:
    """Yield text deltas from the OpenAI Responses API."""
    api_messages = [
        {"role": item["role"], "content": item["content"]}
        for item in messages[-16:]
    ]
    with client.responses.stream(
        model=model,
        instructions=system_instructions(
            module_name, st.session_state.learner_context
        ),
        input=api_messages,
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta


def sidebar() -> tuple[str, bool, str]:
    with st.sidebar:
        st.markdown("## 🪽 Pak Angels")
        st.caption("AI education for every discipline")
        st.divider()
        labels = [f"{module.icon}  {name}" for name, module in MODULES.items()]
        selected_label = st.radio("Learning area", labels, label_visibility="collapsed")
        module_name = list(MODULES)[labels.index(selected_label)]

        st.divider()
        st.markdown("##### Personalize your tutor")
        st.session_state.learner_context = st.text_area(
            "Your discipline and goal",
            value=st.session_state.learner_context,
            placeholder="Example: I study agriculture and want to build a crop-advice app.",
            height=90,
        )

        api_key = secret_value("OPENAI_API_KEY")
        model = secret_value("OPENAI_MODEL", DEFAULT_MODEL)
        demo_mode = not bool(api_key)
        if demo_mode:
            st.info("Demo mode: add an API key in Streamlit Secrets to enable live tutoring.")
        else:
            st.success("Live AI tutor connected")

        if st.button("＋ New conversation", use_container_width=True):
            st.session_state.messages[module_name] = []
            st.rerun()
        st.caption(f"Model: {model}" if not demo_mode else "No API charges in demo mode")
    return module_name, demo_mode, model


def hero(module_name: str) -> None:
    module = MODULES[module_name]
    st.markdown(
        f"""
        <section class="pa-hero">
          <h1>{module.icon} {APP_NAME}</h1>
          <p>{APP_TAGLINE}</p>
          <span class="pa-pill">{module.title}</span>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_home() -> None:
    st.subheader("One guided journey—from an idea to a shared application")
    cols = st.columns(5)
    for col, (name, description) in zip(cols, BUILDER_STEPS):
        with col:
            st.markdown(
                f'<div class="pa-step"><strong>{name}</strong><br><small>{description}</small></div>',
                unsafe_allow_html=True,
            )

    st.markdown("### Explore the program")
    modules = [(name, module) for name, module in MODULES.items() if name != "Home"]
    for start in range(0, len(modules), 3):
        for col, (name, module) in zip(st.columns(3), modules[start : start + 3]):
            with col:
                st.markdown(
                    f'<div class="pa-module"><h3>{module.icon} {name}</h3><p>{module.short_description}</p></div>',
                    unsafe_allow_html=True,
                )

    st.markdown("### AI Application Builder")
    with st.expander("Create my project concept", expanded=False):
        render_builder()


def render_builder() -> None:
    questions = {
        "discipline": "What is your field or discipline?",
        "problem": "What problem do you want to solve?",
        "users": "Who will use the application?",
        "inputs": "What information will users provide?",
        "results": "What should the application produce or accomplish?",
        "actions": "Should it only provide information, or also take actions?",
        "approval": "Which decisions or actions require human approval?",
        "privacy": "What information must remain private?",
        "success": "How will you know the application is successful?",
    }
    with st.form("builder_form"):
        for key, question in questions.items():
            st.session_state.builder_answers[key] = st.text_area(
                question,
                value=st.session_state.builder_answers.get(key, ""),
                height=72,
                key=f"builder_{key}",
            )
        submitted = st.form_submit_button("Create project prompt", type="primary")

    if submitted:
        missing = [question for key, question in questions.items() if not st.session_state.builder_answers.get(key, "").strip()]
        if missing:
            st.warning("Please answer every question so the project prompt has enough information.")
            return
        details = "\n".join(
            f"- {questions[key]} {st.session_state.builder_answers[key].strip()}"
            for key in questions
        )
        prompt = f"""You are an AI solution architect and educator. Convert the following student idea into a concise, implementation-ready MVP specification. Use plain language. Classify it as conventional software, generative AI, single-agent AI, or multi-agent AI, choosing the simplest suitable design. Include the user journey, mandatory features, AI responsibilities, tools, data, privacy, guardrails, human approvals, acceptance tests, required Streamlit files, and deployment requirements. Separate MVP features from later enhancements. Do not generate code yet.\n\n{details}"""
        st.success("Your ChatGPT/Codex project prompt is ready.")
        st.code(prompt, language=None)


def render_module_intro(module_name: str) -> None:
    module = MODULES[module_name]
    st.subheader(module.title)
    st.write(module.short_description)
    st.caption("Topics: " + " • ".join(module.topics))


def render_chat(module_name: str, demo_mode: bool, model: str) -> None:
    module = MODULES[module_name]
    messages = current_messages(module_name)

    st.markdown("#### Try a question")
    selected_prompt = None
    for col, question in zip(st.columns(3), module.starter_questions):
        if col.button(question, use_container_width=True):
            selected_prompt = question

    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    typed_prompt = st.chat_input(f"Ask about {module.title}…")
    prompt = typed_prompt or selected_prompt
    if not prompt:
        return

    messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if demo_mode:
        reply = (
            "**Demo mode is active.** The learning interface is working, but live AI "
            "responses require an `OPENAI_API_KEY` in Streamlit Community Cloud Secrets. "
            "Your question has been saved in this browser session."
        )
        with st.chat_message("assistant"):
            st.info(reply)
        messages.append({"role": "assistant", "content": reply})
        return

    try:
        client = OpenAI(api_key=secret_value("OPENAI_API_KEY"))
        with st.chat_message("assistant"):
            reply = st.write_stream(stream_response(client, model, module_name, messages))
        messages.append({"role": "assistant", "content": str(reply)})
    except Exception as exc:  # Streamlit must present API failures without crashing.
        error_text = str(exc)
        if len(error_text) > 300:
            error_text = error_text[:300] + "…"
        with st.chat_message("assistant"):
            st.error(
                "The tutor could not complete this request. Check the API key, model name, "
                f"and account credits. Technical detail: {error_text}"
            )


def render_about() -> None:
    with st.expander("About Pak Angels and responsible use"):
        st.write(
            "Pak Angels is a Silicon Valley-based global platform supporting AI education, "
            "entrepreneurship, innovation, technology commercialization, and investment "
            "across Pakistan and the global Pakistani community."
        )
        st.markdown(
            '<div class="pa-note"><strong>Important:</strong> This educational tutor may make mistakes. '
            "Verify important information, protect personal data, and obtain qualified human "
            "review for medical, legal, financial, academic, or safety-critical decisions.</div>",
            unsafe_allow_html=True,
        )


def main() -> None:
    apply_theme()
    initialize_state()
    module_name, demo_mode, model = sidebar()
    hero(module_name)
    if module_name == "Home":
        render_home()
    else:
        render_module_intro(module_name)
    render_chat(module_name, demo_mode, model)
    render_about()


if __name__ == "__main__":
    main()

