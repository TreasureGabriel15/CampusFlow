ALLOWED_CATEGORIES = ("Network", "Hardware", "Software", "Other")
ALLOWED_URGENCIES = ("low", "medium", "high")
ALLOWED_STATUSES = ("open", "in_progress", "resolved")


def validate_title(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Title cannot be blank.")
    return value.strip()


def validate_category(value):
    category = value.strip().capitalize() if isinstance(value, str) else ""
    if category not in ALLOWED_CATEGORIES:
        raise ValueError(f"Category must be one of {list(ALLOWED_CATEGORIES)}")
    return category


def validate_urgency(value):
    urgency = value.strip().lower() if isinstance(value, str) else ""
    if urgency not in ALLOWED_URGENCIES:
        raise ValueError(f"Urgency must be one of {list(ALLOWED_URGENCIES)}")
    return urgency


def validate_affected_users(value):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("People affected must be a positive whole number.")
    if value <= 0:
        raise ValueError("People affected must be positive.")
    return value


def validate_staff_name(value):
    name = value.strip() if isinstance(value, str) else ""
    if not name:
        raise ValueError("Staff name cannot be blank.")
    return name


def validate_status(value):
    text = "_".join(
        str(value).strip().lower().replace("-", " ").replace("_", " ").split()
    )
    if text not in ALLOWED_STATUSES:
        raise ValueError("Status must be open, in_progress, or resolved.")
    return text
