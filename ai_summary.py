import os

from dotenv import load_dotenv
from openai import OpenAI

from governance import build_ai_instructions


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_summary_prompt(intake_data, intake_analysis):
    """
    Build a governed prompt for an AI-generated attorney intake summary.

    The AI may organize and summarize intake information but may not
    provide legal advice or make consequential legal decisions.
    """

    governance_instructions = build_ai_instructions()

    missing_required = intake_analysis.get("missing_required", [])
    follow_up_items = intake_analysis.get("follow_up_items", [])

    prompt = f"""
{governance_instructions}

Create a structured Attorney Intake Summary using the information below.

PROSPECTIVE CLIENT INTAKE

Full Name: {intake_data.get("full_name", "Not provided")}
Email: {intake_data.get("email", "Not provided")}
Phone: {intake_data.get("phone", "Not provided")}
Matter Type: {intake_data.get("matter_type", "Not provided")}
Opposing Party: {intake_data.get("opposing_party", "Not provided")}
Incident or Dispute Date: {intake_data.get("incident_date", "Not provided")}

Client Description:
{intake_data.get("description", "Not provided")}

Requested Help:
{intake_data.get("desired_outcome", "Not provided")}

SYSTEM VALIDATION

Intake Status: {intake_analysis.get("intake_status")}
Missing Required Information: {missing_required}
Follow-up Items: {follow_up_items}
Conflict Check Status: {intake_analysis.get("conflict_check_status")}
Decision Status: {intake_analysis.get("decision_status")}

Return the summary using these sections:

Prospective Client
Matter Type
Key Facts Reported
Requested Help
Missing Information / Follow-up
Conflict Check Status
Human Review Status
"""

    return prompt


def generate_ai_summary(intake_data, intake_analysis):
    """
    Send the governed intake prompt to OpenAI and return the summary.
    """

    prompt = build_summary_prompt(intake_data, intake_analysis)

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text