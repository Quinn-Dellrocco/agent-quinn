import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

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
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt, 
            temperature=0
        ),
    )

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print("Prompt tokens: " + str(response.usage_metadata.prompt_token_count))
        print("Response tokens: " + str((response.usage_metadata.total_token_count - response.usage_metadata.prompt_token_count)))
    
    function_results = []

    if response.function_calls:
        for fc in response.function_calls:
            function_call_result = call_function(fc, verbose=args.verbose)
            if not function_call_result.parts:
                raise RuntimeError("Tool result Content.parts was empty")
            function_response = function_call_result.parts[0].function_response
            if function_response is None:
                raise RuntimeError("Tool result Part.function_response was None")
            response_payload = function_response.response
            if response_payload is None:
                raise RuntimeError("Tool FunctionResponse.response was None")
            function_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {response_payload}")
        return
    print(response.text)

if __name__ == "__main__":
    main()
