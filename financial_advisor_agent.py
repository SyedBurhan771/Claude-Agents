"""
Basic Financial Advisor Agent using Claude Agent SDK
This demonstrates a stateless agent using the query() approach
"""

import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock, ResultMessage
from claude_agent_sdk import CLINotFoundError, ProcessError, CLIJSONDecodeError


class FinancialAdvisorAgent:
    """
    A simple financial advisor agent that provides investment advice.
    Uses stateless query approach - no memory between interactions.
    """

    def __init__(self):
        # Define the system prompt for financial advisor behavior
        self.system_prompt = """You are a professional financial advisor with expertise in investment strategies,
portfolio management, and risk assessment. You provide clear, educational financial advice.

When users ask about investments:
- Assess their investment goals and risk tolerance
- Provide balanced analysis of potential investments
- Explain risks and considerations
- Suggest diversification strategies
- Always remind users that this is educational advice, not professional financial planning

Be conversational, helpful, and ensure users understand the risks involved in investing."""

        # Configure the agent options
        self.options = ClaudeAgentOptions(
            system_prompt=self.system_prompt,
            allowed_tools=[],  # No tools needed for basic advice
            permission_mode='default'
        )

    async def ask_advice(self, question: str) -> str:
        """
        Get financial advice for a specific question.
        This is a stateless interaction - no memory of previous questions.

        Args:
            question: The financial question to ask

        Returns:
            The advisor's response as a string
        """
        response_text = ""

        try:
            async for message in query(
                prompt=question,
                options=self.options
            ):
                # Extract text from assistant messages
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            response_text += block.text

                # Check for completion
                if isinstance(message, ResultMessage):
                    if message.is_error:
                        return f"Error occurred: {message.result or 'Unknown error'}"

        except CLINotFoundError:
            return "Error: Claude Code CLI not found. Please install it with: npm install -g @anthropic-ai/claude-code"
        except ProcessError as e:
            return f"Process error: {e.exit_code} - {e.stderr}"
        except CLIJSONDecodeError as e:
            return f"Failed to parse response: {e.line}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

        return response_text


async def main():
    """
    Demonstrate the financial advisor agent with various examples
    """
    print("=" * 70)
    print("Financial Advisor Agent - Stateless Query Demo")
    print("=" * 70)
    print()

    # Create the advisor agent
    advisor = FinancialAdvisorAgent()

    # Example 1: Investment in a specific company
    print("Example 1: Investment in ABC Company")
    print("-" * 70)
    question1 = """
    I have $10,000 that I want to invest in ABC Company stock.
    They are a tech startup that just went public.
    What should I consider before making this investment?
    """
    print(f"Question: {question1.strip()}")
    print()
    print("Advisor Response:")
    response1 = await advisor.ask_advice(question1)
    print(response1)
    print()
    print()

    # Example 2: Portfolio diversification
    print("Example 2: Portfolio Diversification")
    print("-" * 70)
    question2 = """
    I currently have $50,000 invested entirely in tech stocks.
    How should I diversify my portfolio to reduce risk?
    """
    print(f"Question: {question2.strip()}")
    print()
    print("Advisor Response:")
    response2 = await advisor.ask_advice(question2)
    print(response2)
    print()
    print()

    # Example 3: Risk assessment for different investment amounts
    print("Example 3: Investment Amount Analysis")
    print("-" * 70)
    question3 = """
    I'm 30 years old and want to invest $5,000 in the stock market.
    Should I invest it all at once or spread it out over several months?
    """
    print(f"Question: {question3.strip()}")
    print()
    print("Advisor Response:")
    response3 = await advisor.ask_advice(question3)
    print(response3)
    print()
    print()

    # Example 4: Specific company evaluation
    print("Example 4: Company Evaluation - XYZ Corporation")
    print("-" * 70)
    question4 = """
    XYZ Corporation has been showing steady growth of 15% annually for the past 5 years.
    Their P/E ratio is 25 and they pay a 2% dividend.
    I want to invest $20,000. Is this a good investment?
    """
    print(f"Question: {question4.strip()}")
    print()
    print("Advisor Response:")
    response4 = await advisor.ask_advice(question4)
    print(response4)
    print()
    print()

    print("=" * 70)
    print("Demo Complete - Each query was stateless (no memory between questions)")
    print("=" * 70)


async def interactive_mode():
    """
    Interactive mode where users can ask their own questions
    """
    print("=" * 70)
    print("Financial Advisor Agent - Interactive Mode")
    print("=" * 70)
    print("Ask your financial questions. Type 'exit' to quit.")
    print()

    advisor = FinancialAdvisorAgent()

    while True:
        question = input("\nYour Question: ")

        if question.lower() in ['exit', 'quit', 'q']:
            print("Thank you for using the Financial Advisor Agent!")
            break

        if not question.strip():
            continue

        print("\nAdvisor Response:")
        response = await advisor.ask_advice(question)
        print(response)
        print()


if __name__ == "__main__":
    import sys

    # Check if interactive mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        asyncio.run(interactive_mode())
    else:
        asyncio.run(main())
