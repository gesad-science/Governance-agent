import json
from google.adk.agents import LlmAgent

from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

from constraints import CONSTRAINTS

reference_agent = RemoteA2aAgent(
    name="reference_agent",
    description="Agent that receives a text or a bibtex and returns if the references are valid.",
    agent_card=(
        f"http://localhost:8081{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)

def policy_validator(plan_json: dict) -> dict:
    return f'CONSTRAINTS = {CONSTRAINTS}'


INSTRUCTION = """
You are a governance agent responsible for evaluating either plans (JSON format)
or academic executions (plain text).

Step 1. Detect the input type.
  - Try to parse as JSON. If successful, it’s a planning input.
  - If parsing fails, treat as plain text (execution input).

Step 2. If planning:
  - Check that the plan makes logical sense.
  - Verify compliance with policies using the tool `policy_validator`.
  - Check if there is some personal identifiable information (PII) in the plan, if exists it is not valid.
  - Return:
    {
      "type": "planning",
      "is_valid": true/false,
      "policy_violations": [...],
      "logical_issues": [...]
    }

Step 3. If execution:
  - Verify that references are present and plausible using `reference_agent`.
  - Optionally verify writing coherence.
  - Verify if there is some personal identifiable information (PII) in the text, if exists it is not valid.
  - Return:
    {
      "type": "execution",
      "is_valid": true/false,
      "reference_issues": [...],
      "other_issues": [...]
    }
"""

root_agent = LlmAgent(
    name="GovernanceAgent",
    model="gemini-2.0-flash",
    description="Agent that performs governance checks on planning (JSON) or execution (academic text).",
    instruction=INSTRUCTION,
    sub_agents=[reference_agent],
    tools=[policy_validator],
)

#adk run my_agent

