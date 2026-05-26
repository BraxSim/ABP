from __future__ import annotations

from templates import TEMPLATES
from template_selector import assert_template_allowed


def clean_subject(subject: str) -> str:
    subject = subject.strip()

    if subject.lower().startswith("re:"):
        return subject[3:].strip()

    return subject


def render_template(
    template_id: str,
    user_info: dict | None,
    original_subject: str
) -> tuple[str, str]:
    assert_template_allowed(template_id)

    template = TEMPLATES[template_id]

    name = "there"
    plan = "standard"
    profile_link = ""

    if user_info:
        name = user_info.get("name") or "there"
        plan = user_info.get("plan") or "standard"
        profile_link = (
            user_info.get("profile_link")
            or user_info.get("profile_url")
            or user_info.get("link")
            or ""
        )

    variables = {
        "name": name,
        "plan": plan,
        "profile_link": profile_link,
        "original_subject": clean_subject(original_subject),
    }

    subject = template["subject"].format(**variables)
    body = template["body"].format(**variables)

    return subject, body
