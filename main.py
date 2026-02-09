import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_functions import available_functions,call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("Please set your api key.")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    messages =  [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for i in range(20):
        response = client.models.generate_content(
            model='gemini-2.5-flash', contents= messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
            )
        if not response.usage_metadata:
            raise RuntimeError("Metadata is missing.")
        prompt_tokens = response.usage_metadata.prompt_token_count
        responce_tokens = response.usage_metadata.candidates_token_count 

        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

        if args.verbose:
            print(f"User prompt: {args.user_prompt}\n")
            print(f"Prompt tokens: {prompt_tokens}\n")
            print(f"Response tokens: {responce_tokens}\n")

        if not response.function_calls:
            print("Response:")
            print(response.text)
            return
        else:
            function_results = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)

            if not function_call_result.parts:
                raise Exception("Function call returned no parts")

            part = function_call_result.parts[0]

            if part.function_response is None:
                raise Exception("Missing function_response")

            if part.function_response.response is None:
                raise Exception("Function response is empty")

            function_results.append(part)

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

        messages.append(types.Content(role="user", parts=function_results))

    print("The maximum number of iterations is reached")
    exit(1)
    
if __name__ == "__main__":
    main()