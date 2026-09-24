REQUIRED_FIELDS = {
    "full_name": "Full name",
    "email": "Email",
    "matter_type": "Matter type",
    "description": "Description of the matter",
    "acknowledgement": "Acknowledgement",
}


def validate_intake(intake_data):
    """
    Validate a prospective-client intake and identify information
    that staff may need before attorney review.

    This function does not evaluate legal merit or determine whether
    the firm should accept the matter.
    """

    missing_required = []

    for field, label in REQUIRED_FIELDS.items():
        value = intake_data.get(field)

        if not value or not str(value).strip():
            missing_required.append(label)

    follow_up_items = []

    if not intake_data.get("phone", "").strip():
        follow_up_items.append("Phone number not provided")

    if not intake_data.get("opposing_party", "").strip():
        follow_up_items.append(
            "Opposing party not provided — needed for conflict-check preparation"
        )

    if not intake_data.get("incident_date", "").strip():
        follow_up_items.append("Incident or dispute date not provided")

    if not intake_data.get("desired_outcome", "").strip():
        follow_up_items.append("Desired outcome not provided")

    if missing_required:
        intake_status = "Incomplete Intake"
    elif follow_up_items:
        intake_status = "Follow-up Needed"
    else:
        intake_status = "Ready for Human Review"

    return {
        "intake_status": intake_status,
        "missing_required": missing_required,
        "follow_up_items": follow_up_items,
        "conflict_check_status": "Not Performed",
        "decision_status": "No Acceptance Decision Made",
    }