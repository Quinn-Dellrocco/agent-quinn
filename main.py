import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    if api_key == None:
        raise RuntimeError("API key not found")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0),
    )

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print("Prompt tokens: " + str(response.usage_metadata.prompt_token_count))
        print("Response tokens: " + str((response.usage_metadata.total_token_count - response.usage_metadata.prompt_token_count)))
    
    print(response.text)


if __name__ == "__main__":
    main()
