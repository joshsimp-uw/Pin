import re
import json
from pathlib import Path
from typing import Any

def _slug(s: str) -> str:
    s = (s or "").strip().lower()
    s = s.replace("/", " ")
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^a-z0-9_\-]", "", s)
    return s

def get_supported_topics(kb_dir: Path) -> set[str]:
    """Scan KB for specific issue folders (leaf nodes) containing issue.md."""
    topics = set()
    if not kb_dir.exists():
        return topics
    # Only include folders that actually have documentation
    for p in kb_dir.rglob("issue.md"):
        topics.add(_slug(p.parent.name))
    return topics

async def _guess_topic_with_llm(message: str, kb_dir: Path, org_id: str) -> str | None:
    from app.llm.providers import get_llm
    import json

    topics = list(get_supported_topics(kb_dir))
    if not topics:
        return None

    schema = {
        "type": "OBJECT",
        "properties": {
            "matched_folder": {"type": "STRING"}
        },
        "required": ["matched_folder"]
    }

    prompt = (
        f"You are an IT Support Router. User message: '{message}'\n"
        f"Available Support Folders: {', '.join(topics)}\n\n"
        "STRICT RULE: If the user's specific application (e.g., Google Docs) "
        "is NOT in the list above, you MUST return 'unknown'. "
        "Do not attempt to find a 'close' match or a generic category."
    )

    llm = get_llm(org_id=org_id)
    try:
        res = await llm.chat([{"role": "user", "content": prompt}], response_format=schema)
        # Clean the output to ensure case-insensitive matching
        guess = json.loads(res).get("matched_folder", "").strip().lower()
        
        # FUZZY CHECK: If Gemini used dashes instead of underscores, fix it
        guess = guess.replace("-", "_")
        
        return guess if guess in topics else None
    except Exception as e:
        print(f"DEBUG: Mapping failed with error: {e}")
        return None

async def is_supported_request(
    *,
    message: str,
    category: str,
    collected: dict[str, Any],
    kb_dir: Path,
    org_id: str
) -> tuple[bool, str | None]:
    
    # 1. Combine previous answers with the current message
    # If collected has {"error_message": "driver problems"} and message is "USB",
    # full_query becomes: "driver problems Windows HP LaserJet USB"
    context_values = [str(v) for v in collected.values()] if collected else []
    full_query = " ".join(context_values + [message])

    # 2. Pass the enriched query to Gemini instead of just the 1-word answer
    requested_topic = await _guess_topic_with_llm(full_query, kb_dir, org_id)
    
    supported_topics = get_supported_topics(kb_dir)
    if requested_topic and requested_topic in supported_topics:
        return True, None
    
    display_topic = requested_topic if requested_topic and requested_topic != "unknown" else "this issue"
    return False, display_topic
