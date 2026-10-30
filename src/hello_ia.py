from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-6-luna",
    messages=[
        {
            "role": "user",
            "content": "Explica la teoría de la relatividad general en términos sencillos en menos de 100 palabras"
        }
    ]
)

result = response.choices[0].message.content
input_tokens = response.usage.prompt_tokens
output_tokens = response.usage.completion_tokens

print(result)
print(f"Input tokens: {input_tokens}")
print(f"Output tokens: {output_tokens}")
print(f"Total tokens: {input_tokens + output_tokens}")