# Financial Advisor Agent

A comprehensive financial advisor system built with the Claude Agent SDK for Python, demonstrating a **progressive implementation** from basic stateless queries to advanced conversational agents with custom tools.

## 🌟 Features by Stage

### Step 1: Stateless Agent (Basic)
- ✅ Independent queries with no memory
- ✅ Educational financial advice
- ✅ 4 pre-built financial scenarios
- ✅ Interactive Q&A mode

### Step 2: Conversational Agent (Memory)
- ✅ Multi-turn conversations with context retention
- ✅ Advisor remembers client details across exchanges
- ✅ Context-aware recommendations
- ✅ Natural conversation flow

### Step 3: Financial Tools
- ✅ Portfolio allocation calculator (age-based)
- ✅ Compound interest projections
- ✅ Stock metrics evaluation (P/E, dividend, growth)
- ✅ Retirement planning calculator
- ✅ Investment comparison tool

### Advanced: Complete System (Memory + Tools)
- ✅ **Full conversational memory**
- ✅ **Custom financial calculations**
- ✅ **Data-driven recommendations**
- ✅ **Context synthesis across conversation**

## 📋 Prerequisites

### Required Software

1. **Claude Code CLI**:
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

2. **Python 3.8+**:
   ```bash
   python --version  # Verify installation
   ```

### Authentication

```bash
claude auth login
```

## 🚀 Quick Start

### Installation

```bash
# Navigate to project directory
cd D:\Claude-Agent

# Install dependencies
pip install -r requirements.txt


```

This launches an interactive menu with all available examples:
- Step 1: Stateless demos
- Step 2: Conversational demos
- Step 3: Tools demos
- Advanced: Full system demos
- Comparison mode

**Or run specific scripts:**

```bash
# Step 1: Basic stateless agent
python financial_advisor.py
python financial_advisor.py --interactive

# Step 2: Conversational with memory
python conversational_advisor.py
python conversational_advisor.py --interactive

# Step 3: Financial tools
python financial_tools.py

# Advanced: Full system (RECOMMENDED)
python advanced_advisor.py
python advanced_advisor.py --interactive
```

## 📊 Architecture Comparison

| Feature | Step 1<br/>(Stateless) | Step 2<br/>(Memory) | Step 3<br/>(Tools) | Advanced<br/>(Complete) |
|---------|---------|---------|---------|---------|
| **SDK Approach** | `query()` | `ClaudeSDKClient` | `query()` + tools | `ClaudeSDKClient` + tools |
| **Conversation Memory** | ❌ | ✅ | ❌ | ✅ |
| **Custom Tools** | ❌ | ❌ | ✅ | ✅ |
| **Context Retention** | ❌ | ✅ | ❌ | ✅ |
| **Financial Calculations** | ❌ | ❌ | ✅ | ✅ |
| **Best For** | Quick advice | Ongoing planning | Calculations | Complete planning |

## 🔧 Available Financial Tools

When using Step 3 or Advanced mode, the advisor has access to:

### 1. Portfolio Allocation Calculator
```python
calculate_portfolio_allocation(
    age=35,
    risk_tolerance="aggressive",
    total_amount=50000
)
```
Provides age-appropriate asset allocation recommendations.

### 2. Compound Interest Calculator
```python
calculate_compound_interest(
    principal=10000,
    annual_rate=8,
    years=20,
    monthly_contribution=500
)
```
Projects investment growth over time with contributions.

### 3. Stock Metrics Evaluator
```python
evaluate_stock_metrics(
    stock_name="TechCorp",
    current_price=125,
    pe_ratio=22,
    dividend_yield=2.5,
    revenue_growth=18,
    debt_to_equity=0.8
)
```
Analyzes fundamental metrics and provides evaluation.

### 4. Retirement Planning Calculator
```python
calculate_retirement_needs(
    current_age=35,
    retirement_age=65,
    current_savings=50000,
    desired_annual_income=80000,
    expected_return=7
)
```
Calculates required retirement corpus and monthly savings.

### 5. Investment Comparison
```python
compare_investment_options(
    option_a_name="S&P 500",
    option_a_return=7,
    option_a_risk="low",
    option_b_name="Tech ETF",
    option_b_return=10,
    option_b_risk="high",
    investment_amount=20000,
    time_horizon=10
)
```
Side-by-side comparison of two investment choices.

## 💡 Usage Examples

### Example 1: Basic Advice (Step 1)
```bash
python financial_advisor.py
```
- 4 pre-built scenarios
- No memory between questions
- Fast and simple

### Example 2: Multi-Turn Conversation (Step 2)
```bash
python conversational_advisor.py
```
- Advisor remembers your details
- Natural conversation flow
- Context-aware recommendations

### Example 3: With Calculations (Step 3)
```bash
python financial_tools.py
```
- Precise portfolio allocations
- Growth projections
- Stock evaluations

### Example 4: Complete Planning Session (Advanced)
```bash
python advanced_advisor.py
```
**This is the recommended version!**
- Full conversation memory
- Custom financial tools
- Data-driven recommendations
- Synthesizes all information

**Interactive Mode:**
```bash
python advanced_advisor.py --interactive
```
Have a real conversation with full features enabled.

## 📁 Project Structure

```
D:\Claude-Agent/
├── financial_advisor.py          # Step 1: Stateless agent
├── conversational_advisor.py     # Step 2: With memory
├── financial_tools.py             # Step 3: Custom tools
├── advanced_advisor.py            # Advanced: Memory + Tools
├── requirements.txt               # Dependencies
├── README.md                      # This file
```

## 🎯 How It Works

### Step 1: Stateless Query Pattern
```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="Investment advice?",
    options=ClaudeAgentOptions(system_prompt="...")
):
    # Process response
```
- Simple one-shot queries
- No state management
- Quick answers

### Step 2: Conversational Pattern
```python
from claude_agent_sdk import ClaudeSDKClient

async with ClaudeSDKClient(options=options) as client:
    await client.query("First question")
    async for msg in client.receive_response():
        # Process

    await client.query("Follow-up")  # Remembers context!
    async for msg in client.receive_response():
        # Process
```
- Maintains conversation state
- Context across multiple exchanges
- Natural dialogue

### Step 3: Tools Pattern
```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("tool_name", "description", {"param": type})
async def my_tool(args):
    # Calculate something
    return {"content": [{"type": "text", "text": result}]}

server = create_sdk_mcp_server(name="finance", tools=[my_tool])
options = ClaudeAgentOptions(
    mcp_servers={"finance": server},
    allowed_tools=["mcp__finance__tool_name"]
)
```
- Custom financial calculations
- Data-driven insights
- Precise recommendations

### Advanced: Combined Pattern
```python
# Combines ClaudeSDKClient + Tools
client = ClaudeSDKClient(options=options_with_tools)
await client.query("Complex financial planning question")
# Agent uses tools AND remembers context!
```

## 🎓 Learning Path

**Recommended progression:**

1. **Start with Step 1** (`financial_advisor.py`)
   - Understand basic query pattern
   - See simple advice examples

2. **Move to Step 2** (`conversational_advisor.py`)
   - Learn conversation management
   - See how memory improves UX

3. **Explore Step 3** (`financial_tools.py`)
   - Understand tool creation
   - See calculation examples

4. **Master Advanced** (`advanced_advisor.py`)
   - Combine all concepts
   - Build complete systems

## 🐛 Troubleshooting

### Common Issues

**"Claude Code not found"**
```bash
npm install -g @anthropic-ai/claude-code
```

**"Not authenticated"**
```bash
claude auth login
```

**"Module not found: claude_agent_sdk"**
```bash
pip install claude-agent-sdk
```

**"Import error: financial_tools"**
```bash
# Make sure you're in the project directory
cd D:\Claude-Agent
python advanced_advisor.py
```

### Testing Your Setup

```bash
# Quick verification
python quick_test.py

# Should print a short financial advice response
```

## ⚠️ Important Notes

### Authentication
The Claude Code CLI handles API authentication automatically. Ensure you're logged in with `claude auth login`.

### Rate Limits
Be mindful of API usage, especially in interactive modes. The SDK respects Claude API rate limits.

### Data Privacy
All conversations are processed through the Claude API. Don't share real account numbers or sensitive personal information in examples.

## 🔗 Resources

- [Claude Agent SDK Python Docs](https://platform.claude.com/docs/en/agent-sdk/python)
- [Claude Code Documentation](https://code.claude.com/docs)
- [API Reference](https://platform.claude.com/docs/en/agent-sdk/python)
- [GitHub Issues](https://github.com/anthropics/claude-code/issues)

## 🚀 Next Steps

Want to extend this project? Ideas:

## 📄 License

This is a demonstration project for learning purposes. See individual files for more details.

---

**Built with ❤️ using Claude Agent SDK**
