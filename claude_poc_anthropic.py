import os
from anthropic import Anthropic
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
# Initialize the client (automatically reads ANTHROPIC_API_KEY from environment)
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

if not client.api_key:
    print("ERROR: ANTHROPIC_API_KEY not found! Set it in your terminal first.")
    exit(1)

# Your test message
user_message = "Hello Claude! Tell me a very short joke about Python programming."

print("=== TESTING CLAUDE API POC ===\n")

# 1. List all available models and pick the latest Sonnet
print("1. Fetching available models...")
selected_model = None
try:
    models_response = client.models.list()
    print("Available Models:")
    sonnet_models = []
    for model in models_response.data:
        model_id = model.id
        print(f"   • {model_id}")
        if hasattr(model, 'context_window'):
            print(f"     → Context window: {model.context_window} tokens")
        # Collect Sonnet models (sort by date in ID for latest)
        if "sonnet" in model_id.lower():
            sonnet_models.append(model_id)
    
    # Pick the latest Sonnet (highest date in ID)
    if sonnet_models:
        selected_model = max(sonnet_models)  # Sorts lexicographically; dates are YYYYMMDD so it works
        print(f"\n   → Auto-selected latest Sonnet: {selected_model}")
    else:
        selected_model = "claude-sonnet-4-5-20250929"  # Fallback to a recent one from your output
        print(f"\n   → Using fallback Sonnet: {selected_model}")
        
except Exception as e:
    print(f"Failed to list models: {e}")
    selected_model = "claude-sonnet-4-5-20250929"  # Use this if list fails

# 2. Count tokens (now using selected_model)
print("\n2. Counting tokens for your message...")
try:
    token_count = client.messages.count_tokens(
        model=selected_model,
        messages=[{"role": "user", "content": user_message}]
    )
    print(f"Estimated input tokens: {token_count.input_tokens}")
except Exception as e:
    print(f"Token counting failed: {e}")

# 3. Actually send the message and get response
print("\n3. Sending message to Claude...")
try:
    response = client.messages.create(
        model=selected_model,
        max_tokens=1024,
        temperature=0.7,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    print("\nClaude's Reply:")
    print(response.content[0].text)

    print("\nToken Usage:")
    print(f"   Input tokens : {response.usage.input_tokens}")
    print(f"   Output tokens: {response.usage.output_tokens}")
    print(f"   Total tokens : {response.usage.input_tokens + response.usage.output_tokens}")

except Exception as e:
    print(f"API call failed: {e}")
    print("Common fixes: wrong API key, rate limit, or check model in Step 1")

print("\nPOC Completed Successfully!")