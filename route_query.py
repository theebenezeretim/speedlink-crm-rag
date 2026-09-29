"""Conversation-aware service hints. Unknown queries remain searchable."""
import re


def normalize(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def contains(text, phrase):
    return f" {normalize(phrase)} " in f" {normalize(text)} "


WORKSPACE_TYPES = {
    "shared coworking space": ("shared coworking", "shared workspace", "shared space", "shared desk"),
    "personal workspace": ("personal workspace", "personal office", "private office", "personal desk"),
    "executive office": ("executive office",),
    "ceo executive office": ("ceo", "ceo executive office"),
    "boardroom": ("boardroom", "board room", "meeting room"),
    "training halls": ("training hall", "training halls", "training room"),
    "computer training hall": ("computer training hall", "computer hall", "computer lab"),
    "mini training hall": ("mini training hall", "mini hall"),
    "ict simulation room": ("ict simulation room", "simulation room"),
}

SERVICE_TERMS = {
    "workspace": ("workspace", "work space", "coworking", "co working", "desk", "office space",
                  "place to work", "somewhere to work", "workplace", "work station", "remote worker"),
    "ftth internet": ("internet", "wifi", "wi fi", "fiber", "fibre", "ftth", "broadband",
                      "smart starter", "smart premium", "smart diamond", "smart gold", "router"),
    "training": ("training", "course", "courses", "learn", "teach", "class", "classes", "certification",
                 "data analytics", "web development", "ui ux", "cybersecurity", "cloud computing",
                 "digital marketing", "graphics design", "mobile app development", "solar systems", "siwes"),
    "pearson vue": ("pearson", "vue", "exam", "exams", "test center", "test centre"),
    "research": ("research", "thesis", "dissertation", "project", "topic", "proposal", "literature review",
                 "methodology", "data analysis", "prototype", "supervisor", "postgraduate", "phd",
                 "msc", "journal", "nda", "arduino", "matlab", "simulation"),
}


def workspace_types(query):
    text = normalize(query)
    found = []
    aliases = sorted(((alias, kind) for kind, names in WORKSPACE_TYPES.items() for alias in names),
                     key=lambda item: len(item[0]), reverse=True)
    for alias, kind in aliases:
        if contains(text, alias):
            if kind not in found:
                found.append(kind)
            text = re.sub(r"\b" + re.escape(normalize(alias)) + r"\b", " ", text)
    return tuple(found)


def detect_services(query):
    text = normalize(query)
    found = []
    kinds = workspace_types(text)
    if kinds:
        found.append("workspace")
        for names in WORKSPACE_TYPES.values():
            for alias in sorted(names, key=len, reverse=True):
                text = re.sub(r"\b" + re.escape(normalize(alias)) + r"\b", " ", text)
    # These phrases are research context, not requests to buy training.
    for phrase in ("course of study", "training data", "machine learning model"):
        text = text.replace(phrase, " ")
    if any(contains(text, word) for word in SERVICE_TERMS["pearson vue"]):
        found.append("pearson vue")
        text = re.sub(r"\bcertification\b", " ", text)
    for service in ("research", "ftth internet", "training", "workspace"):
        if any(contains(text, word) for word in SERVICE_TERMS[service]) and service not in found:
            found.append(service)
    if kinds and "ftth internet" in found and not any(contains(query, phrase) for phrase in
            ("and internet", "also internet", "ftth", "broadband", "internet plans")):
        found.remove("ftth internet")  # Internet as a room amenity.
    if "workspace" in found and "training" in found and contains(query, "for training"):
        found.remove("training")
    # An office may just be the installation location ("internet for my office").
    if not found and contains(text, "office"):
        found.append("workspace")
    return tuple(found)


def resolve_services(query, chat_history=()):
    explicit = detect_services(query)
    if explicit:
        return explicit
    if normalize(query) in {"hi", "hello", "good morning", "good afternoon", "good evening"}:
        return ()
    if contains(query, "services") and not explicit:
        return ()
    for message in reversed(list(chat_history)[-12:]):
        if message.get("role") == "user":
            previous = detect_services(message.get("content", ""))
            if previous:
                return previous
    return ()


def detect_service(query, chat_history=()):
    """Compatibility helper; use detect_services for multiple service requests."""
    services = resolve_services(query, chat_history)
    return services[0] if services else "unknown"
