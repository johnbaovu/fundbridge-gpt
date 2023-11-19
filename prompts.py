from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain

earnings_prompt_template = """Summarize key takeaways in the transcript of an earnings call.  In your summary, address the following points about financial performance metrics one-by-one.

- Financial ratios highlighted and their implications
- Any comparisons of financial metrics to previous quarters (quarter-over-quarter) or years (year-over-year).
- Performance of any major business lines discussed.
- Any significant changes in operating income and free cashflow and their potential causes.
- Extract mentions of returning cash to shareholders through dividends or share buybacks.
- Discuss the company's budgeting and forecasting approaches mentioned.
- Discuss significant strategic initiatives or changes.  Discuss any new business ventures or mergers and acquisitions.

Additional Guidelines:

- Present points in bullet point form only.
- Include as much detail as possible. More detail is better.
- Include numeric figures where relevant.

TRANSCRIPT:
{text}

Respond with the following headers:
------------
FINANCIAL PERFORMANCE & METRICS:

BUSINESS LINE PERFORMANCE:

OPERATING INCOME & CASH FLOW:

SHAREHOLDER RETURN:

FINANCIAL FORECASTS:

STRATEGIC MATTERS OR MERGERS & ACQUISITIONS:

"""

PROMPT_earnings = PromptTemplate(template=earnings_prompt_template,
                        input_variables=["text"])



