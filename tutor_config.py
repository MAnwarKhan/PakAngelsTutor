"""Learning content and system instructions for the Pak Angels AI Tutor."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LearningModule:
    icon: str
    title: str
    short_description: str
    topics: tuple[str, ...]
    starter_questions: tuple[str, ...]
    instructions: str


BASE_INSTRUCTIONS = """
You are Pak Angels AI Tutor, an encouraging, practical AI educator serving
students, faculty, professionals, entrepreneurs, and startup founders. Teach
instead of merely answering. Use plain language first, define technical terms,
and adapt explanations to the learner's stated background. Provide actionable
examples, short exercises, and checkpoints when helpful.

Never claim that generated code is automatically correct, secure, or ready for
high-stakes use. Encourage testing, human review, privacy protection, responsible
AI, and consultation with qualified professionals for medical, legal, financial,
or safety-critical decisions. Never request passwords, private keys, or sensitive
personal data. When generating code, never hardcode credentials; use environment
variables or Streamlit secrets. Keep recommendations realistic for learners with
limited budgets and connectivity.
""".strip()


MODULES: dict[str, LearningModule] = {
    "Home": LearningModule(
        "🏠",
        "Welcome",
        "Start learning or choose a practical AI project.",
        ("Program orientation", "Learning pathways", "Responsible AI", "Project selection"),
        (
            "Help me choose the right learning path.",
            "Suggest an AI project for my field.",
            "Explain how this tutor can help me.",
        ),
        "Orient the learner, learn their discipline and goals, and recommend a small achievable next step.",
    ),
    "AI-101 Foundations": LearningModule(
        "🧠",
        "AI-101 Foundations",
        "Understand AI, machine learning, large language models, ethics, and careers.",
        ("Artificial intelligence", "Machine learning", "Deep learning", "LLMs", "Responsible AI", "AI careers"),
        (
            "What is artificial intelligence?",
            "Explain AI, machine learning, and generative AI with examples.",
            "How can students use AI responsibly?",
        ),
        "Teach foundational AI concepts with familiar, discipline-neutral examples. Check understanding without assuming programming knowledge.",
    ),
    "Prompt Engineering": LearningModule(
        "✍️",
        "Prompt Engineering",
        "Write clear prompts that produce useful, structured, and repeatable results.",
        ("Context", "Roles", "Constraints", "Examples", "Output formats", "Prompt evaluation"),
        (
            "Teach me a simple formula for writing good prompts.",
            "Improve a prompt for my project.",
            "Create a reusable research prompt template.",
        ),
        "Coach the learner through goal, context, constraints, examples, and output format. Explain why each revision improves the prompt.",
    ),
    "Generative AI": LearningModule(
        "✨",
        "Generative AI",
        "Use AI to create and transform text, images, code, and other content.",
        ("Generative models", "Text generation", "Image generation", "Code generation", "Productivity", "Evaluation"),
        (
            "How does generative AI work?",
            "Suggest generative AI uses for my discipline.",
            "How should I evaluate AI-generated content?",
        ),
        "Teach generative AI through practical creation tasks. Emphasize verification, attribution, consent, and limitations.",
    ),
    "Agentic AI": LearningModule(
        "🤖",
        "Agentic AI",
        "Design AI systems that plan, use tools, and complete supervised workflows.",
        ("Goals", "Planning", "Tools", "Memory", "Guardrails", "Human approval", "Evaluation"),
        (
            "What makes an AI application agentic?",
            "Design a safe single-agent workflow for my idea.",
            "Where should a human approve an agent's actions?",
        ),
        "Teach agents as models with instructions, tools, state, and a controlled loop. Prefer a deterministic workflow or one agent before multi-agent complexity. Always identify approval gates and failure modes.",
    ),
    "RAG": LearningModule(
        "📚",
        "Retrieval-Augmented Generation",
        "Build assistants that answer from approved documents and knowledge sources.",
        ("Documents", "Chunking", "Embeddings", "Retrieval", "Citations", "Evaluation"),
        (
            "Explain RAG without technical jargon.",
            "Design a document assistant for my organization.",
            "How do I test whether retrieved answers are reliable?",
        ),
        "Explain retrieval before generation, source grounding, citations, and evaluation. Distinguish RAG from fine-tuning and ordinary prompting.",
    ),
    "Multi-Agent Systems": LearningModule(
        "👥",
        "Multi-Agent Systems",
        "Coordinate specialized agents only when separate roles add real value.",
        ("Roles", "Routing", "Handoffs", "Supervisor patterns", "Quality control", "Cost"),
        (
            "When should I use more than one agent?",
            "Design a research and review agent team.",
            "Simplify my multi-agent idea.",
        ),
        "Teach routing, manager, and handoff patterns. Challenge unnecessary multi-agent designs and explain their cost, latency, and reliability tradeoffs.",
    ),
    "AI Workflow Design": LearningModule(
        "🔀",
        "AI Workflow Design",
        "Turn a real problem into clear steps, decisions, approvals, and outcomes.",
        ("Problem definition", "Inputs and outputs", "Decision points", "Human review", "Errors", "Monitoring"),
        (
            "Convert my problem into an AI workflow.",
            "Design a human-in-the-loop workflow.",
            "Help me identify workflow risks and exceptions.",
        ),
        "Guide the learner from problem to actors, inputs, steps, decisions, exceptions, approvals, outputs, and measures of success.",
    ),
    "Business Automation": LearningModule(
        "⚙️",
        "Business Process Automation",
        "Improve repetitive work while preserving accountability and human control.",
        ("Process discovery", "Document processing", "Customer support", "Sales", "HR", "Finance", "Operations"),
        (
            "Which process should my organization automate first?",
            "Design an invoice-processing workflow.",
            "Create a safe customer-support automation plan.",
        ),
        "Focus on measurable operational problems, exception handling, auditability, permissions, and responsible adoption—not automation for its own sake.",
    ),
    "Streamlit Development": LearningModule(
        "💻",
        "Streamlit Development",
        "Build approachable Python web applications and deploy them from GitHub.",
        ("Python basics", "Widgets", "Session state", "APIs", "Secrets", "Testing", "Deployment"),
        (
            "Build my first Streamlit application.",
            "Explain the files needed for Streamlit Community Cloud.",
            "Help me fix a Streamlit error.",
        ),
        "Teach in small runnable increments. Provide complete files when requested, explain what changed, protect secrets, and include verification steps.",
    ),
    "AI Startup Mentor": LearningModule(
        "🚀",
        "AI Startup Mentor",
        "Validate an idea, define an MVP, and prepare for responsible launch.",
        ("Problem validation", "Customer discovery", "MVP", "Business model", "Go-to-market", "Pitching"),
        (
            "Evaluate my startup idea.",
            "Create a customer-discovery plan.",
            "Turn my idea into an achievable MVP.",
        ),
        "Be a constructive startup mentor. Separate assumptions from evidence and prioritize customer validation before extensive development.",
    ),
}


BUILDER_STEPS = (
    ("IDEA", "Describe the problem, users, inputs, desired results, and human decisions."),
    ("DESIGN", "Create and approve a concise application blueprint."),
    ("BUILD", "Generate the smallest working version, then add AI capabilities."),
    ("TEST", "Test the main journey, errors, safety, privacy, and usefulness."),
    ("SHARE", "Publish through GitHub and Streamlit Community Cloud."),
)


def system_instructions(module_name: str, learner_context: str = "") -> str:
    """Return the combined tutor instructions for a learning module."""
    module = MODULES.get(module_name, MODULES["Home"])
    context = learner_context.strip() or "The learner has not provided background information yet."
    return f"{BASE_INSTRUCTIONS}\n\nSelected learning area: {module.title}\n{module.instructions}\n\nLearner context: {context}"

