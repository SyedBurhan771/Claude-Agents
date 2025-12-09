"""
Advanced Financial Advisor - Steps 2 + 3 Combined
Conversational agent WITH memory AND custom financial tools
This is the most powerful version of the financial advisor.
"""

import asyncio
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ToolResultBlock,
    ResultMessage
)
from financial_tools import create_financial_tools_server


class AdvancedFinancialAdvisor:
    """
    Full-featured financial advisor with:
    - Conversational memory (ClaudeSDKClient)
    - Custom financial calculation tools
    - Context-aware recommendations
    """

    def __init__(self):
        # Create financial tools server
        self.financial_server = create_financial_tools_server()

        # System prompt that guides tool usage
        self.system_prompt = """You are an expert financial advisor with access to advanced calculation tools.
You maintain context across conversations and use your tools to provide data-driven advice.

Your capabilities:
- Remember client details: age, income, savings, goals, risk tolerance
- Use tools to perform accurate financial calculations
- Build personalized recommendations based on conversation history
- Reference previous advice when new information emerges

Available tools:
- calculate_portfolio_allocation: Age-based asset allocation recommendations
- calculate_compound_interest: Project investment growth with contributions
- evaluate_stock_metrics: Analyze stock fundamentals (P/E, dividend, growth, debt)
- calculate_retirement_needs: Calculate retirement corpus and monthly savings needed
- compare_investment_options: Side-by-side comparison of two investment choices

Best practices:
- Use tools proactively when calculations would help
- Reference previous conversation context in your recommendations
- Synthesize tool results with your expertise
- Explain the reasoning behind recommendations
- Always include appropriate risk disclaimers

Be conversational, thorough, and always remember what the client has shared."""

        # Configure options with tools enabled
        self.options = ClaudeAgentOptions(
            system_prompt=self.system_prompt,
            mcp_servers={"finance": self.financial_server},
            allowed_tools=[
                "mcp__finance__calculate_portfolio_allocation",
                "mcp__finance__calculate_compound_interest",
                "mcp__finance__evaluate_stock_metrics",
                "mcp__finance__calculate_retirement_needs",
                "mcp__finance__compare_investment_options"
            ],
            permission_mode='default'
        )

        self.client = None

    async def start_conversation(self):
        """Start a new conversation session."""
        self.client = ClaudeSDKClient(options=self.options)
        await self.client.connect()

    async def ask(self, question: str, show_tool_usage: bool = True) -> str:
        """
        Ask a question in the ongoing conversation.

        Args:
            question: The question to ask
            show_tool_usage: Whether to print tool usage information

        Returns:
            The advisor's response as a string
        """
        if not self.client:
            raise RuntimeError("Conversation not started. Call start_conversation() first.")

        response_text = ""

        try:
            await self.client.query(question)

            async for message in self.client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            response_text += block.text
                        elif isinstance(block, ToolUseBlock) and show_tool_usage:
                            print(f"  [🔧 Using tool: {block.name}]")
                        elif isinstance(block, ToolResultBlock) and show_tool_usage:
                            print(f"  [✓ Tool completed]")

                if isinstance(message, ResultMessage):
                    if message.is_error:
                        return f"Error: {message.result or 'Unknown error'}"

        except Exception as e:
            return f"Error: {str(e)}"

        return response_text

    async def end_conversation(self):
        """End the conversation."""
        if self.client:
            await self.client.disconnect()
            self.client = None


async def demo_full_financial_planning():
    """
    Demonstrate a complete financial planning conversation with tools and memory
    """
    print("=" * 80)
    print("ADVANCED FINANCIAL ADVISOR - Full Demo")
    print("Conversational Memory + Custom Tools")
    print("=" * 80)
    print()

    advisor = AdvancedFinancialAdvisor()

    try:
        await advisor.start_conversation()

        # Turn 1: Initial client profile
        print("🗣️  Turn 1: Client Introduction")
        print("-" * 80)
        question1 = """Hi! I'm Sarah, 35 years old. I just got promoted and now make $120,000 per year.
        I have $40,000 in savings that I want to invest. I consider myself moderately aggressive
        with my risk tolerance. Can you help me create an investment plan?"""

        print(f"Client: {question1}")
        print()
        print("Advisor: ", end="", flush=True)
        response1 = await advisor.ask(question1)
        print(response1)
        print()
        print()

        # Turn 2: Ask about specific allocation (should use portfolio allocation tool)
        print("🗣️  Turn 2: Requesting Specific Allocation")
        print("-" * 80)
        question2 = """Based on my age and risk tolerance, what should my exact portfolio allocation be?"""

        print(f"Client: {question2}")
        print()
        print("Advisor: ", end="", flush=True)
        response2 = await advisor.ask(question2)
        print(response2)
        print()
        print()

        # Turn 3: Long-term growth projection
        print("🗣️  Turn 3: Growth Projection")
        print("-" * 80)
        question3 = """If I invest that $40,000 and add $1,000 per month, how much will I have in 25 years
        assuming 8% returns?"""

        print(f"Client: {question3}")
        print()
        print("Advisor: ", end="", flush=True)
        response3 = await advisor.ask(question3)
        print(response3)
        print()
        print()

        # Turn 4: Retirement planning (should remember age from Turn 1)
        print("🗣️  Turn 4: Retirement Planning")
        print("-" * 80)
        question4 = """I want to retire at 65 with $80,000 per year in income. Based on everything
        we discussed, am I on track? How much should I save monthly?"""

        print(f"Client: {question4}")
        print()
        print("Advisor: ", end="", flush=True)
        response4 = await advisor.ask(question4)
        print(response4)
        print()
        print()

        # Turn 5: Stock evaluation
        print("🗣️  Turn 5: Specific Stock Evaluation")
        print("-" * 80)
        question5 = """I'm considering buying stock in my company. They have:
        - Current price: $85
        - P/E ratio: 28
        - Dividend yield: 1.2%
        - Revenue growth: 25%
        - Debt-to-equity: 0.4

        Should I invest some of my allocation in this stock?"""

        print(f"Client: {question5}")
        print()
        print("Advisor: ", end="", flush=True)
        response5 = await advisor.ask(question5)
        print(response5)
        print()
        print()

        # Turn 6: Investment comparison (remembers context)
        print("🗣️  Turn 6: Comparing Investment Options")
        print("-" * 80)
        question6 = """I'm debating between putting $20,000 into:
        Option A: S&P 500 index fund (7% return, low risk)
        Option B: Tech sector ETF (10% return, high risk)

        Which makes more sense for me given everything we've discussed?"""

        print(f"Client: {question6}")
        print()
        print("Advisor: ", end="", flush=True)
        response6 = await advisor.ask(question6)
        print(response6)
        print()
        print()

        # Turn 7: Summary and action plan (synthesizes entire conversation)
        print("🗣️  Turn 7: Action Plan Request")
        print("-" * 80)
        question7 = """Can you give me a complete action plan based on everything we discussed?
        I want concrete steps to follow."""

        print(f"Client: {question7}")
        print()
        print("Advisor: ", end="", flush=True)
        response7 = await advisor.ask(question7)
        print(response7)
        print()

    finally:
        await advisor.end_conversation()

    print()
    print("=" * 80)
    print("COMPLETE FINANCIAL PLANNING SESSION FINISHED")
    print("=" * 80)
    print()
    print("✨ Features Demonstrated:")
    print("  ✓ Conversational memory across 7 turns")
    print("  ✓ Portfolio allocation calculation")
    print("  ✓ Compound interest projections")
    print("  ✓ Retirement planning calculations")
    print("  ✓ Stock metrics evaluation")
    print("  ✓ Investment comparison")
    print("  ✓ Context-aware recommendations")
    print("  ✓ Synthesized action plan")
    print()


async def demo_portfolio_review_with_tools():
    """
    Demonstrate an existing portfolio review using tools
    """
    print("\n" + "=" * 80)
    print("PORTFOLIO REVIEW WITH TOOLS")
    print("=" * 80)
    print()

    advisor = AdvancedFinancialAdvisor()

    try:
        await advisor.start_conversation()

        print("Client provides current holdings...")
        print("-" * 80)
        question1 = """I'm 42 years old with moderate risk tolerance. My current portfolio is:
        - $60,000 in various stocks
        - $25,000 in bonds
        - $15,000 in cash

        Total: $100,000

        Is this allocation appropriate for my age?"""

        print(f"Client: {question1}")
        print()
        print("Advisor: ", end="", flush=True)
        response1 = await advisor.ask(question1)
        print(response1)
        print()
        print()

        print("Client asks about rebalancing...")
        print("-" * 80)
        question2 = """What changes should I make to rebalance my portfolio?"""

        print(f"Client: {question2}")
        print()
        print("Advisor: ", end="", flush=True)
        response2 = await advisor.ask(question2)
        print(response2)
        print()

    finally:
        await advisor.end_conversation()


async def interactive_advanced_advisor():
    """
    Interactive mode with full features
    """
    print("=" * 80)
    print("ADVANCED INTERACTIVE FINANCIAL ADVISOR")
    print("=" * 80)
    print()
    print("Features enabled:")
    print("  ✓ Conversational memory - I'll remember everything you tell me")
    print("  ✓ Financial tools - I can calculate allocations, growth, and more")
    print("  ✓ Personalized advice - Based on your unique situation")
    print()
    print("Commands:")
    print("  'exit' - End conversation")
    print("  'summary' - Get conversation summary")
    print()

    advisor = AdvancedFinancialAdvisor()

    try:
        await advisor.start_conversation()
        turn_count = 0

        while True:
            turn_count += 1
            question = input(f"\n[Turn {turn_count}] You: ")

            if question.lower() in ['exit', 'quit', 'q']:
                print("\n✓ Thank you for the consultation!")
                break

            if question.lower() == 'summary':
                question = "Can you summarize everything we've discussed so far and the key recommendations?"

            if not question.strip():
                continue

            print(f"\n[Turn {turn_count}] Advisor: ", end="", flush=True)
            response = await advisor.ask(question, show_tool_usage=True)
            print(response)

    except KeyboardInterrupt:
        print("\n\nConversation interrupted.")
    finally:
        await advisor.end_conversation()


async def main():
    """Run demonstrations"""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        await interactive_advanced_advisor()
    else:
        # Run full demo
        await demo_full_financial_planning()

        # Short pause
        await asyncio.sleep(1)

        # Portfolio review demo
        await demo_portfolio_review_with_tools()

        print()
        print("=" * 80)
        print("🎉 ADVANCED ADVISOR DEMO COMPLETE")
        print("=" * 80)
        print()
        print("This advanced advisor combines:")
        print("  • Step 1: Stateless queries ✓")
        print("  • Step 2: Conversational memory ✓")
        print("  • Step 3: Custom financial tools ✓")
        print()
        print("Try interactive mode:")
        print("  python advanced_advisor.py --interactive")
        print()


if __name__ == "__main__":
    asyncio.run(main())
