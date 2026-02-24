import asyncio
from agents import summary_agent, action_agent, risk_agent

SAMPLE_DOC = """
Meeting: Project Alpha (2026-02-24)
Attendees: Venkata (PM), Sayan (Dev)
Budget: $150K. Launch: Q2 2026.

Actions:
- Venkata: Budget by 2026-03-10 (High)
- Sayan: UI prototype by 2026-03-15 (depends: budget)

Risks: Vendor unconfirmed (High), tight timeline.
"""

async def test_agents():
    print("🧪 Testing Summary...")
    aresult = await summary_agent.run(task=SAMPLE_DOC)
    summary_output = aresult.messages[-1].content
    print("Summary:", str(summary_output)[:200], "...\n")

    print("🧪 Testing Actions...")
    aresult = await action_agent.run(task=SAMPLE_DOC)
    actions_output = aresult.messages[-1].content
    print("Actions JSON:", str(actions_output), "\n")

    print("🧪 Testing Risks...")
    aresult = await risk_agent.run(task=SAMPLE_DOC)
    risks_output = aresult.messages[-1].content
    print("Risks JSON:", str(risks_output))

if __name__ == "__main__":
    asyncio.run(test_agents())
