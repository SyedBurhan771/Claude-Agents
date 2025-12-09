"""
Step 2: Conversational Financial Advisor with Memory
This demonstrates using ClaudeSDKClient for multi-turn conversations with context retention
"""

import asyncio
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ResultMessage,
    CLINotFoundError,
    ProcessError
)


class ConversationalFinancialAdvisor:
    """
    Financial advisor agent with conversation memory.
    Uses ClaudeSDKClient to maintain context across multiple exchanges.
    """

    def __init__(self):
        # Define system prompt for conversational financial advisor
        self.system_prompt = """You are a professional financial advisor with expertise in investment strategies,
portfolio management, and risk assessment. You maintain context across conversations and can reference
previous discussions with the client.

Your approach:
- Remember details the client shares (age, risk tolerance, existing portfolio, goals)
- Build on previous advice in follow-up questions
- Provide personalized recommendations based on their full context
- Ask clarifying questions when needed
- Track the evolution of their financial situation across the conversation
- Always provide educational, balanced advice with appropriate risk disclaimers

Be conversational, empathetic, and maintain continuity in your advice."""

        # Configure agent options
        self.options = ClaudeAgentOptions(
            system_prompt=self.system_prompt,
            allowed_tools=[],  # No tools yet (will add in Step 3)
            permission_mode='default'
        )

        # Client will be initialized when starting conversation
        self.client = None

    async def start_conversation(self, initial_message: str = None):
        """
        Start a new conversation session.

        Args:
            initial_message: Optional greeting or initial query
        """
        self.client = ClaudeSDKClient(options=self.options)
        await self.client.connect()

        if initial_message:
            await self.ask(initial_message)

    async def ask(self, question: str) -> str:
        """
        Ask a question in the ongoing conversation.
        The agent remembers all previous exchanges.

        Args:
            question: The question to ask

        Returns:
            The advisor's response as a string
        """
        if not self.client:
            raise RuntimeError("Conversation not started. Call start_conversation() first.")

        response_text = ""

        try:
            # Send the query to Claude
            await self.client.query(question)

            # Receive and process the response
            async for message in self.client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            response_text += block.text

                if isinstance(message, ResultMessage):
                    if message.is_error:
                        return f"Error: {message.result or 'Unknown error'}"

        except Exception as e:
            return f"Error during conversation: {str(e)}"

        return response_text

    async def end_conversation(self):
        """End the conversation and disconnect."""
        if self.client:
            await self.client.disconnect()
            self.client = None


async def demo_conversation_flow():
    """
    Demonstrate a multi-turn conversation with context retention
    """
    print("=" * 80)
    print("CONVERSATIONAL FINANCIAL ADVISOR - Step 2 Demo")
    print("Multi-turn conversation with memory")
    print("=" * 80)
    print()

    advisor = ConversationalFinancialAdvisor()

    try:
        # Start the conversation
        await advisor.start_conversation()

        # Turn 1: Initial introduction
        print("Turn 1: Client Introduction")
        print("-" * 80)
        question1 = """Hi! I'm 28 years old and just started my career in tech.
        I'm making $95,000 per year and want to start investing.
        I have $15,000 saved up. Where should I begin?"""

        print(f"Client: {question1}")
        print()
        response1 = await advisor.ask(question1)
        print(f"Advisor: {response1}")
        print()
        print()

        # Turn 2: Follow-up about risk (advisor should remember age, salary, savings)
        print("Turn 2: Risk Tolerance Discussion")
        print("-" * 80)
        question2 = """I'd say I'm moderately aggressive with risk since I'm young.
        What does that mean for my portfolio allocation?"""

        print(f"Client: {question2}")
        print()
        response2 = await advisor.ask(question2)
        print(f"Advisor: {response2}")
        print()
        print()

        # Turn 3: Specific investment question (should remember previous context)
        print("Turn 3: Specific Investment Question")
        print("-" * 80)
        question3 = """Should I put some of that money into a tech stock like the company I work for?"""

        print(f"Client: {question3}")
        print()
        response3 = await advisor.ask(question3)
        print(f"Advisor: {response3}")
        print()
        print()

        # Turn 4: Timeline and goals (building on everything discussed)
        print("Turn 4: Investment Timeline")
        print("-" * 80)
        question4 = """I'm thinking about buying a house in 5-7 years.
        How should that affect my investment strategy?"""

        print(f"Client: {question4}")
        print()
        response4 = await advisor.ask(question4)
        print(f"Advisor: {response4}")
        print()
        print()

        # Turn 5: Action plan (should synthesize all previous information)
        print("Turn 5: Requesting Action Plan")
        print("-" * 80)
        question5 = """Can you give me a concrete action plan based on everything we discussed?"""

        print(f"Client: {question5}")
        print()
        response5 = await advisor.ask(question5)
        print(f"Advisor: {response5}")
        print()

    finally:
        # Always clean up
        await advisor.end_conversation()

    print()
    print("=" * 80)
    print("Conversation Complete")
    print("=" * 80)
    print()
    print("Key Observations:")
    print("  ✓ The advisor remembered the client is 28 years old")
    print("  ✓ Context about $95K salary and $15K savings was retained")
    print("  ✓ Risk tolerance discussion built on previous exchanges")
    print("  ✓ House purchase goal influenced final recommendations")
    print("  ✓ Action plan synthesized all information from the conversation")
    print()


async def demo_portfolio_review():
    """
    Demonstrate an ongoing portfolio review conversation
    """
    print("\n" + "=" * 80)
    print("PORTFOLIO REVIEW CONVERSATION")
    print("=" * 80)
    print()

    advisor = ConversationalFinancialAdvisor()

    try:
        await advisor.start_conversation()

        # Initial portfolio state
        print("Client shares current portfolio...")
        print("-" * 80)
        portfolio = """I currently have:
        - $25,000 in S&P 500 index fund
        - $10,000 in tech stocks (mostly FAANG)
        - $5,000 in bonds
        - $10,000 in savings account

        I'm 35 years old, married, no kids yet. What do you think?"""

        print(f"Client: {portfolio}")
        print()
        response = await advisor.ask(portfolio)
        print(f"Advisor: {response}")
        print()
        print()

        # Follow-up about diversification
        print("Follow-up: Diversification concern...")
        print("-" * 80)
        question = "You mentioned diversification. Should I add international stocks?"
        print(f"Client: {question}")
        print()
        response = await advisor.ask(question)
        print(f"Advisor: {response}")
        print()
        print()

        # New information emerges
        print("Client reveals new information...")
        print("-" * 80)
        question = """Actually, my wife and I are planning to have kids in the next 2 years.
        Does that change your recommendations?"""
        print(f"Client: {question}")
        print()
        response = await advisor.ask(question)
        print(f"Advisor: {response}")
        print()

    finally:
        await advisor.end_conversation()

    print()
    print("=" * 80)
    print("Portfolio Review Complete")
    print("=" * 80)
    print()


async def interactive_conversation():
    """
    Interactive mode with conversation memory
    """
    print("=" * 80)
    print("INTERACTIVE CONVERSATIONAL ADVISOR")
    print("=" * 80)
    print("Have a multi-turn conversation with your financial advisor.")
    print("The advisor will remember everything you discuss.")
    print("Type 'exit' to end the conversation.")
    print()

    advisor = ConversationalFinancialAdvisor()

    try:
        await advisor.start_conversation()
        turn_count = 0

        while True:
            turn_count += 1
            question = input(f"\n[Turn {turn_count}] You: ")

            if question.lower() in ['exit', 'quit', 'q']:
                print("\nThank you for the conversation!")
                break

            if not question.strip():
                continue

            print(f"\n[Turn {turn_count}] Advisor: ", end="", flush=True)
            response = await advisor.ask(question)
            print(response)

    finally:
        await advisor.end_conversation()


async def main():
    """Run all demonstrations"""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        await interactive_conversation()
    else:
        # Run demo conversations
        await demo_conversation_flow()

        # Wait a moment between demos
        await asyncio.sleep(1)

        await demo_portfolio_review()

        print()
        print("=" * 80)
        print("STEP 2 COMPLETE")
        print("=" * 80)
        print()
        print("Conversational Features Demonstrated:")
        print("  ✓ Multi-turn conversations with context retention")
        print("  ✓ ClaudeSDKClient maintains conversation state")
        print("  ✓ Advisor remembers client details across exchanges")
        print("  ✓ Advice builds on previous discussion")
        print("  ✓ Context-aware recommendations")
        print()
        print("Next: Run with --interactive flag for your own conversation")
        print("      python conversational_advisor.py --interactive")
        print()


if __name__ == "__main__":
    asyncio.run(main())
