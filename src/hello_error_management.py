from openai import OpenAI, AuthenticationError, RateLimitError, APIConnectionError
from dotenv import load_dotenv

load_dotenv()

def call_ai(question: str) -> str:
    client = OpenAI()
    try:
        response = client.chat.completions.create(
            model="gpt-6-luna",
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_completion_tokens=1400,
            temperature=1,
        )
        return response.choices[0].message.content
    except AuthenticationError:
        return "Authentication error occurred."
    except RateLimitError:
        return "Rate limit error occurred."
    except APIConnectionError:
        return "API connection error occurred."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

if __name__ == "__main__":
    response = call_ai("Cual es el mayor divulgador de ciencia español vivo")
    print(f"AI response: {response}")

