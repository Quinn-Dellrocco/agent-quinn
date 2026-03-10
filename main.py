import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

MAX_ITERS = 20

def main():
    if api_key == None:
        raise RuntimeError("API key not found")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for i in range(MAX_ITERS):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0,
            ),
        )
    
        if args.verbose:
            print(f"\n--- Iteration {i + 1}/{MAX_ITERS} ---")
            print(f"User prompt: {args.user_prompt}")

            if getattr(response, "usage_metadata", None):
                prompt_tokens = response.usage_metadata.prompt_token_count
                total_tokens = response.usage_metadata.total_token_count
                print("Prompt tokens:", prompt_tokens)
                print("Response tokens:", total_tokens - prompt_tokens)

        candidates = getattr(response, "candidates", None) or []

        if not candidates:
            raise RuntimeError("No candidates returned by model")

        for cand in candidates:
            if cand and cand.content:
                messages.append(cand.content)

        if response.function_calls:
            function_responses = []

            for fc in response.function_calls:
                function_call_result = call_function(fc, verbose=args.verbose)

                if not function_call_result.parts:
                    raise RuntimeError("Tool result Content.parts was empty")

                function_response = function_call_result.parts[0].function_response
                if function_response is None:
                    raise RuntimeError("Tool result Part.function_response was None")

                payload = function_response.response
                if payload is None:
                    raise RuntimeError("Tool FunctionResponse.response was None")

                function_responses.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {payload}")

            messages.append(types.Content(role="user", parts=function_responses))

            continue

        print("Final response:")
        print(response.text)
        return

    print(f"Error: Reached max iterations ({MAX_ITERS}) without a final response.")
    sys.exit(1)

if __name__ == "__main__":
    main()
