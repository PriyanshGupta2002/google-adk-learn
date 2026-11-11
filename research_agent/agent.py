from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.agents.sequential_agent import SequentialAgent

MODEL = "gemini-3.8-flash"

company_agent = Agent(
    model=MODEL,
    name="company_agent",
    description="Researches company information",
    instruction="""
    Research the company's history, founders, leadership,
    products and business operations.

    Use Google Search to find current and reliable information.
    Include sources and relevant dates in your report.
    """,
    tools=[google_search],
    output_key="company_report",
)


financial_agent = Agent(
    model=MODEL,
    name="finance_agent",
    description="Researches about financial company information",
    instruction="""
You are a Financial Research Analyst.

Research the company's financial performance using Google Search.

Cover:
1. Annual revenue and revenue growth.
2. Net income and operating profit.
3. Quarterly financial results.
4. Cash flow and debt.
5. Stock performance (if publicly listed).
6. Financial risks and future outlook.

Prioritize official annual reports, investor relations
websites and SEC filings.

Mention reporting periods, currencies and dates.
Never invent financial figures.
""",
    tools=[google_search],
    output_key="financial_report",
)


technology_agent = Agent(
    model=MODEL,
    name="technology_research_agent",
    description="Researches a company's technology stack, products, innovations and competitive technology landscape.",
    instruction="""
    You are a Technology Research Analyst.

    Research the company's technology ecosystem using Google Search.

    Cover the following areas:

    1. Core Technologies:
       Research the major technologies, hardware, software,
       platforms and infrastructure developed or used by the company.

    2. Products and Services:
       Identify the company's major technology products
       and explain their technical capabilities.

    3. Technology Stack:
       Identify programming languages, frameworks,
       platforms, cloud infrastructure and tools where
       reliable public information is available.

    4. Innovation and R&D:
       Research recent technological innovations,
       patents, research initiatives and product launches.

    5. Technology Ecosystem:
       Research developer tools, APIs, partnerships,
       integrations and ecosystem adoption.

    6. Competitor Analysis:
       Compare the company's technology with major
       competitors and explain its technical advantages
       and limitations.

    7. Future Roadmap:
       Identify publicly announced future technologies,
       upcoming products and strategic technology directions.

    Research using Google Search.
    Prioritize official documentation, engineering blogs,
    technical publications and credible sources.

    Clearly distinguish verified facts from analysis.
    Include source links and publication dates.
    Do not invent technical specifications or claims.

    Return a structured technology research report.
    """,
    tools=[google_search],
    output_key="technology_report",
)

parallel_research_agent = ParallelAgent(
    name="parallel_research_agent",
    sub_agents=[
        company_agent,
        financial_agent,
        technology_agent,
    ],
)


summary_agent = Agent(
    model=MODEL,
    name="summary_agent",
    description="Combines research reports into a comprehensive company report.",
    instruction="""
    You are a Senior Research Analyst.

    You will receive three research reports:

    1. Company Report: {company_report}
    2. Financial Report: {financial_report}
    3. Technology Report: {technology_report}

    Your task is to combine these reports into one
    comprehensive research report.

    Structure your final report into:

    1. Company Overview
    2. Financial Analysis
    3. Technology Analysis
    4. Competitive Position
    5. Key Findings
    6. Overall Conclusion

    Do not invent information.
    Highlight missing or conflicting information.
    Preserve source links and dates from the original reports.
    """,
    output_key="final_report",
)

research_workflow = SequentialAgent(
    name="company_research_system",
    description="Researches any company using parallel specialized research agents and generates a comprehensive report.",
    sub_agents=[
        parallel_research_agent,
        summary_agent,
    ],
)

router_agent = Agent(
    model=MODEL,
    name="router_agent",
    description="Routes user requests to the appropriate workflow.",
    instruction="""
    You are the main assistant and request router.

    Your responsibilities:

    1. If the user sends a greeting like Hi, Hello,
       or asks a general question, respond normally.
       Do not start company research.

    2. If the user wants company research but has
       not specified a company, ask them which
       company they want to research.

    3. If the user explicitly requests research
       about a specific company, delegate the task
       to company_research_workflow.

    4. Never execute the research workflow for
       greetings or unrelated questions.

    Be friendly and concise.
    """,
    sub_agents=[research_workflow],
)

root_agent = router_agent
