"""
Step 3: Custom Financial Tools
Implements financial calculation tools using @tool decorator and MCP servers
"""

import asyncio
from typing import Any
from claude_agent_sdk import (
    tool,
    create_sdk_mcp_server,
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ResultMessage
)


# ============================================================================
# Financial Calculation Tools
# ============================================================================

@tool(
    "calculate_portfolio_allocation",
    "Calculate recommended portfolio allocation based on age and risk tolerance",
    {
        "age": int,
        "risk_tolerance": str,  # "conservative", "moderate", "aggressive"
        "total_amount": float
    }
)
async def calculate_portfolio_allocation(args: dict[str, Any]) -> dict[str, Any]:
    """
    Calculate portfolio allocation using age-based rule with risk adjustment.
    Formula: Stock % = (100 - age) adjusted for risk tolerance
    """
    age = args["age"]
    risk = args["risk_tolerance"].lower()
    total = args["total_amount"]

    # Base allocation using "100 minus age" rule
    base_stock_pct = 100 - age

    # Adjust for risk tolerance
    if risk == "conservative":
        stock_pct = max(20, base_stock_pct - 15)
    elif risk == "aggressive":
        stock_pct = min(90, base_stock_pct + 15)
    else:  # moderate
        stock_pct = base_stock_pct

    bond_pct = 100 - stock_pct

    # Calculate dollar amounts
    stock_amount = total * (stock_pct / 100)
    bond_amount = total * (bond_pct / 100)

    result = f"""Portfolio Allocation Recommendation:

Age: {age} years old
Risk Tolerance: {risk.title()}
Total Investment: ${total:,.2f}

RECOMMENDED ALLOCATION:
- Stocks/Equities: {stock_pct}% (${stock_amount:,.2f})
- Bonds/Fixed Income: {bond_pct}% (${bond_amount:,.2f})

BREAKDOWN SUGGESTION:
Stocks portion:
  - 70% Diversified Index Funds (${stock_amount * 0.7:,.2f})
  - 20% International Stocks (${stock_amount * 0.2:,.2f})
  - 10% Individual Stocks (${stock_amount * 0.1:,.2f})

Bonds portion:
  - 60% Government Bonds (${bond_amount * 0.6:,.2f})
  - 40% Corporate Bonds (${bond_amount * 0.4:,.2f})

Note: This is a general guideline. Actual allocation should be adjusted based on individual circumstances."""

    return {
        "content": [{
            "type": "text",
            "text": result
        }]
    }


@tool(
    "calculate_compound_interest",
    "Calculate compound interest and future value of investments",
    {
        "principal": float,
        "annual_rate": float,  # as percentage (e.g., 7 for 7%)
        "years": int,
        "monthly_contribution": float
    }
)
async def calculate_compound_interest(args: dict[str, Any]) -> dict[str, Any]:
    """
    Calculate compound interest with monthly contributions.
    """
    principal = args["principal"]
    annual_rate = args["annual_rate"] / 100  # Convert percentage to decimal
    years = args["years"]
    monthly_contrib = args["monthly_contribution"]

    # Monthly rate
    monthly_rate = annual_rate / 12
    months = years * 12

    # Future value of initial principal
    fv_principal = principal * ((1 + monthly_rate) ** months)

    # Future value of monthly contributions (annuity formula)
    if monthly_contrib > 0:
        fv_contributions = monthly_contrib * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    else:
        fv_contributions = 0

    total_fv = fv_principal + fv_contributions
    total_invested = principal + (monthly_contrib * months)
    total_gains = total_fv - total_invested

    result = f"""Investment Growth Projection:

INITIAL INVESTMENT: ${principal:,.2f}
MONTHLY CONTRIBUTION: ${monthly_contrib:,.2f}
ANNUAL RETURN RATE: {args['annual_rate']}%
TIME PERIOD: {years} years

RESULTS:
Total Amount Invested: ${total_invested:,.2f}
Future Value: ${total_fv:,.2f}
Total Investment Gains: ${total_gains:,.2f}
Return on Investment: {(total_gains / total_invested * 100):.2f}%

YEAR-BY-YEAR BREAKDOWN:"""

    # Year by year breakdown (show every 5 years for long periods)
    step = 5 if years > 10 else 1
    result += "\n"

    for year in range(step, years + 1, step):
        months_elapsed = year * 12
        fv_p = principal * ((1 + monthly_rate) ** months_elapsed)
        if monthly_contrib > 0:
            fv_c = monthly_contrib * (((1 + monthly_rate) ** months_elapsed - 1) / monthly_rate)
        else:
            fv_c = 0
        total_value = fv_p + fv_c
        result += f"\nYear {year}: ${total_value:,.2f}"

    return {
        "content": [{
            "type": "text",
            "text": result
        }]
    }


@tool(
    "evaluate_stock_metrics",
    "Evaluate if a stock's metrics indicate good value",
    {
        "stock_name": str,
        "current_price": float,
        "pe_ratio": float,
        "dividend_yield": float,
        "revenue_growth": float,  # as percentage
        "debt_to_equity": float
    }
)
async def evaluate_stock_metrics(args: dict[str, Any]) -> dict[str, Any]:
    """
    Analyze stock metrics and provide evaluation.
    """
    name = args["stock_name"]
    price = args["current_price"]
    pe = args["pe_ratio"]
    div_yield = args["dividend_yield"]
    revenue_growth = args["revenue_growth"]
    debt_to_equity = args["debt_to_equity"]

    # Evaluation logic
    signals = []

    # P/E Ratio analysis
    if pe < 15:
        signals.append("✓ P/E Ratio: ATTRACTIVE (< 15) - Stock may be undervalued")
    elif pe < 25:
        signals.append("○ P/E Ratio: FAIR (15-25) - Reasonably valued")
    else:
        signals.append("⚠ P/E Ratio: HIGH (> 25) - Stock may be overvalued or high-growth")

    # Dividend yield
    if div_yield > 3:
        signals.append("✓ Dividend Yield: STRONG (> 3%) - Good income potential")
    elif div_yield > 1:
        signals.append("○ Dividend Yield: MODERATE (1-3%) - Some income")
    else:
        signals.append("○ Dividend Yield: LOW (< 1%) - Growth-focused company")

    # Revenue growth
    if revenue_growth > 20:
        signals.append("✓ Revenue Growth: EXCELLENT (> 20%) - Strong expansion")
    elif revenue_growth > 10:
        signals.append("✓ Revenue Growth: GOOD (10-20%) - Solid growth")
    elif revenue_growth > 0:
        signals.append("○ Revenue Growth: MODEST (0-10%) - Stable company")
    else:
        signals.append("⚠ Revenue Growth: DECLINING - Revenue concerns")

    # Debt analysis
    if debt_to_equity < 0.5:
        signals.append("✓ Debt Level: LOW (< 0.5) - Strong balance sheet")
    elif debt_to_equity < 1.5:
        signals.append("○ Debt Level: MODERATE (0.5-1.5) - Manageable debt")
    else:
        signals.append("⚠ Debt Level: HIGH (> 1.5) - Leverage concerns")

    # Overall assessment
    positive_signals = sum(1 for s in signals if s.startswith("✓"))
    warning_signals = sum(1 for s in signals if s.startswith("⚠"))

    if positive_signals >= 3:
        overall = "POSITIVE - Multiple favorable indicators"
    elif warning_signals >= 2:
        overall = "CAUTIOUS - Multiple concerns identified"
    else:
        overall = "NEUTRAL - Mixed signals, requires deeper analysis"

    result = f"""Stock Evaluation: {name}

CURRENT METRICS:
Price: ${price:.2f}
P/E Ratio: {pe:.2f}
Dividend Yield: {div_yield:.2f}%
Revenue Growth: {revenue_growth:.2f}%
Debt-to-Equity: {debt_to_equity:.2f}

ANALYSIS:
{chr(10).join(signals)}

OVERALL ASSESSMENT: {overall}

IMPORTANT: This is a simplified analysis based on limited metrics. Always conduct
thorough research including industry comparison, competitive analysis, management
quality, and market conditions before investing."""

    return {
        "content": [{
            "type": "text",
            "text": result
        }]
    }


@tool(
    "calculate_retirement_needs",
    "Calculate retirement savings needed and monthly savings required",
    {
        "current_age": int,
        "retirement_age": int,
        "current_savings": float,
        "desired_annual_income": float,  # in retirement
        "expected_return": float  # annual percentage
    }
)
async def calculate_retirement_needs(args: dict[str, Any]) -> dict[str, Any]:
    """
    Calculate retirement savings goals and required monthly contributions.
    """
    current_age = args["current_age"]
    retirement_age = args["retirement_age"]
    current_savings = args["current_savings"]
    annual_income = args["desired_annual_income"]
    expected_return = args["expected_return"] / 100

    years_to_retirement = retirement_age - current_age
    life_expectancy = 90  # Assume living to 90
    retirement_years = life_expectancy - retirement_age

    # Calculate retirement corpus needed (using 4% withdrawal rule as baseline)
    retirement_corpus = annual_income * 25  # 25x annual expenses for 4% withdrawal

    # Calculate future value of current savings
    fv_current = current_savings * ((1 + expected_return) ** years_to_retirement)

    # Additional savings needed
    additional_needed = retirement_corpus - fv_current

    # Calculate monthly contribution needed
    if additional_needed > 0:
        monthly_rate = expected_return / 12
        months = years_to_retirement * 12
        # PMT formula: needed = PMT * (((1 + r)^n - 1) / r)
        monthly_contribution = (additional_needed * monthly_rate) / (((1 + monthly_rate) ** months - 1))
    else:
        monthly_contribution = 0

    result = f"""Retirement Planning Analysis:

YOUR PROFILE:
Current Age: {current_age}
Retirement Age: {retirement_age}
Years Until Retirement: {years_to_retirement}
Current Savings: ${current_savings:,.2f}
Expected Annual Return: {args['expected_return']}%

RETIREMENT GOALS:
Desired Annual Income: ${annual_income:,.2f}
Estimated Retirement Duration: {retirement_years} years (to age 90)

CALCULATIONS:
Retirement Corpus Needed: ${retirement_corpus:,.2f}
  (Based on 4% withdrawal rule: 25x annual income)

Future Value of Current Savings: ${fv_current:,.2f}
  (Your ${current_savings:,.2f} growing at {args['expected_return']}% for {years_to_retirement} years)

Additional Savings Needed: ${max(0, additional_needed):,.2f}

MONTHLY SAVINGS REQUIRED: ${monthly_contribution:,.2f}

PROJECTION:
If you save ${monthly_contribution:,.2f} per month for {years_to_retirement} years
at {args['expected_return']}% annual return, you will have:
  ${retirement_corpus:,.2f} at age {retirement_age}

This will provide ${annual_income:,.2f} per year for {retirement_years} years.

Note: This assumes constant returns and doesn't account for inflation.
Consider consulting a financial advisor for personalized planning."""

    return {
        "content": [{
            "type": "text",
            "text": result
        }]
    }


@tool(
    "compare_investment_options",
    "Compare two investment options side by side",
    {
        "option_a_name": str,
        "option_a_return": float,  # expected annual return %
        "option_a_risk": str,  # "low", "medium", "high"
        "option_b_name": str,
        "option_b_return": float,
        "option_b_risk": str,
        "investment_amount": float,
        "time_horizon": int  # years
    }
)
async def compare_investment_options(args: dict[str, Any]) -> dict[str, Any]:
    """
    Compare two investment options.
    """
    name_a = args["option_a_name"]
    return_a = args["option_a_return"] / 100
    risk_a = args["option_a_risk"]
    name_b = args["option_b_name"]
    return_b = args["option_b_return"] / 100
    risk_b = args["option_b_risk"]
    amount = args["investment_amount"]
    years = args["time_horizon"]

    # Calculate future values
    fv_a = amount * ((1 + return_a) ** years)
    fv_b = amount * ((1 + return_b) ** years)
    gain_a = fv_a - amount
    gain_b = fv_b - amount

    # Risk scoring
    risk_scores = {"low": 1, "medium": 2, "high": 3}
    risk_score_a = risk_scores.get(risk_a.lower(), 2)
    risk_score_b = risk_scores.get(risk_b.lower(), 2)

    # Risk-adjusted return (simple Sharpe-like ratio)
    risk_adj_return_a = (args["option_a_return"] - 2) / risk_score_a  # 2% risk-free rate assumption
    risk_adj_return_b = (args["option_b_return"] - 2) / risk_score_b

    result = f"""Investment Comparison Analysis:

Initial Investment: ${amount:,.2f}
Time Horizon: {years} years

{'='*70}
OPTION A: {name_a}
{'='*70}
Expected Return: {args['option_a_return']}% annually
Risk Level: {risk_a.upper()}
Future Value: ${fv_a:,.2f}
Total Gain: ${gain_a:,.2f}
Risk-Adjusted Return Score: {risk_adj_return_a:.2f}

{'='*70}
OPTION B: {name_b}
{'='*70}
Expected Return: {args['option_b_return']}% annually
Risk Level: {risk_b.upper()}
Future Value: ${fv_b:,.2f}
Total Gain: ${gain_b:,.2f}
Risk-Adjusted Return Score: {risk_adj_return_b:.2f}

{'='*70}
COMPARISON
{'='*70}
"""

    if fv_a > fv_b:
        difference = fv_a - fv_b
        result += f"{name_a} will be ${difference:,.2f} higher than {name_b}\n"
    else:
        difference = fv_b - fv_a
        result += f"{name_b} will be ${difference:,.2f} higher than {name_a}\n"

    # Recommendation
    if risk_adj_return_a > risk_adj_return_b * 1.2:
        result += f"\nRECOMMENDATION: {name_a} offers better risk-adjusted returns"
    elif risk_adj_return_b > risk_adj_return_a * 1.2:
        result += f"\nRECOMMENDATION: {name_b} offers better risk-adjusted returns"
    else:
        result += f"\nRECOMMENDATION: Both options are comparable; choose based on your risk tolerance"

    result += "\n\nNote: Past performance doesn't guarantee future results. Consider diversification."

    return {
        "content": [{
            "type": "text",
            "text": result
        }]
    }


# ============================================================================
# Create MCP Server with all financial tools
# ============================================================================

def create_financial_tools_server():
    """
    Create an MCP server with all financial calculation tools.

    Returns:
        McpSdkServerConfig: Configured server with financial tools
    """
    return create_sdk_mcp_server(
        name="financial_tools",
        version="1.0.0",
        tools=[
            calculate_portfolio_allocation,
            calculate_compound_interest,
            evaluate_stock_metrics,
            calculate_retirement_needs,
            compare_investment_options
        ]
    )


# ============================================================================
# Demo usage of tools
# ============================================================================

async def demo_tools():
    """
    Demonstrate the financial tools in action
    """
    print("=" * 80)
    print("FINANCIAL TOOLS - Step 3 Demo")
    print("=" * 80)
    print()

    # Create the financial tools server
    financial_server = create_financial_tools_server()

    # Configure agent with tools
    system_prompt = """You are a financial advisor with access to powerful calculation tools.
When clients ask about investments, portfolios, or retirement planning, use the available
tools to provide accurate calculations and data-driven recommendations.

Available tools:
- calculate_portfolio_allocation: Get age-appropriate asset allocation
- calculate_compound_interest: Project investment growth over time
- evaluate_stock_metrics: Analyze stock fundamental metrics
- calculate_retirement_needs: Plan for retirement savings
- compare_investment_options: Compare two investment choices

Always use tools when numerical calculations would help the client."""

    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        mcp_servers={"finance": financial_server},
        allowed_tools=[
            "mcp__finance__calculate_portfolio_allocation",
            "mcp__finance__calculate_compound_interest",
            "mcp__finance__evaluate_stock_metrics",
            "mcp__finance__calculate_retirement_needs",
            "mcp__finance__compare_investment_options"
        ],
        permission_mode='default'
    )

    # Example 1: Portfolio allocation
    print("Example 1: Portfolio Allocation")
    print("-" * 80)
    query1 = """I'm 32 years old with aggressive risk tolerance.
    I have $50,000 to invest. What should my portfolio allocation be?"""

    print(f"Query: {query1}")
    print()
    print("Response:")
    async for message in query(prompt=query1, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
                elif isinstance(block, ToolUseBlock):
                    print(f"[Using tool: {block.name}]")
        if isinstance(message, ResultMessage) and message.is_error:
            print(f"Error: {message.result}")

    print()
    print()

    # Example 2: Compound interest calculation
    print("Example 2: Investment Growth Projection")
    print("-" * 80)
    query2 = """If I invest $10,000 today and add $500 per month,
    how much will I have in 20 years assuming 8% annual returns?"""

    print(f"Query: {query2}")
    print()
    print("Response:")
    async for message in query(prompt=query2, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
                elif isinstance(block, ToolUseBlock):
                    print(f"[Using tool: {block.name}]")

    print()
    print()

    # Example 3: Stock evaluation
    print("Example 3: Stock Metrics Evaluation")
    print("-" * 80)
    query3 = """Evaluate this stock for me:
    Company: TechCorp
    Price: $125
    P/E Ratio: 22
    Dividend Yield: 2.5%
    Revenue Growth: 18%
    Debt-to-Equity: 0.8

    Is this a good investment?"""

    print(f"Query: {query3}")
    print()
    print("Response:")
    async for message in query(prompt=query3, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
                elif isinstance(block, ToolUseBlock):
                    print(f"[Using tool: {block.name}]")

    print()
    print()

    print("=" * 80)
    print("STEP 3 TOOLS DEMO COMPLETE")
    print("=" * 80)
    print()


if __name__ == "__main__":
    asyncio.run(demo_tools())
