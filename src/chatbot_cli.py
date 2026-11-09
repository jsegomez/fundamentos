"""
Proyecto: CLI Chatbot
"""
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuracion
MODEL = "gpt-6-luna"

SYSTEM_PROMPT = """Eres un asistente técnico experto en Python e IA.
Eres directo, usas ejemplos de código cuando es relevante,
y respondes en el mismo idioma que el usuario.
Si no sabes algo, lo dices honestamente."""

# Costos de la API en USD
INPUT_COST = 0.10
OUTPUT_COST = 0.5

class Chatbot:
    def __init__(self, system_prompt: str = SYSTEM_PROMPT):
        self.client = OpenAI()
        self.model = MODEL
        self.history: list[dict] = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        self.total_tokens = 0
        self.total_cost = 0.0

    def chat(self, usr_message: str) -> str:
        """Envía un mensaje del usuario al modelo y devuelve la respuesta, manteniendo el historial de la conversación."""

        self.history.append({
            "role": "user",
            "content": usr_message
        })

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.history,
            max_completion_tokens=1000,
            temperature=1,
        )

        ai_message = response.choices[0].message.content
        self.history.append({
            "role": "assistant",
            "content": ai_message
        })

        self._update_cost(response.usage)
        return ai_message

    def _update_cost(self, usage) -> None:
        """Actualiza el costo total y el total de tokens usados según el uso proporcionado."""
        input_cost = (usage.prompt_tokens / 1_000_000) * INPUT_COST
        output_cost = (usage.completion_tokens / 1_000_000) * OUTPUT_COST
        self.total_tokens += usage.total_tokens
        self.total_cost += input_cost + output_cost

    def show_stats(self) -> None:
        """Muestra las estadísticas actuales de tokens y costos."""
        print(f"Total de turnos: {len(self.history) // 2}")
        print(f"Total tokens usados: {self.total_tokens}")
        print(f"Total costo estimado: ${self.total_cost:.6f}")
    

def main():
    """Función principal"""
    print("╔══════════════════════════════════════╗")
    print("║      Python IA Aplicada - Chatbot    ║")
    print("║  Escribe 'quit' o Ctrl+C para salir  ║")
    print("╚══════════════════════════════════════╝\n")

    bot = Chatbot()

    try:
        while True:
            try:
                user_input = input("Tú: ").strip()
            except EOFError as e:
                print(f"Error: {e}")
                break
            if user_input.lower() in ["quit", "exit", "q", "bye", "salir"]:
                print("Saliendo del chatbot. ¡Hasta luego!")
                break
            if not user_input:
                continue
            if user_input.lower() == "/stats":
                bot.show_stats()
                continue
            if user_input.lower() == "/reset":
                bot.history = []
                bot.total_tokens = 0
                bot.total_cost = 0.0
                print("Nueva conversación iniciada.")
                continue
            print("\nIA: ", end="", flush=True)

            try:
                ai_response = bot.chat(user_input)
                print(ai_response.encode('utf-8', errors='replace').decode('utf-8'))
                print(f"Total tokens usados: {bot.total_tokens}")
                print(f"Total costo estimado: ${bot.total_cost:.4f} USD")
            except Exception as e:
                print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nSaliendo del chatbot. ¡Hasta luego!")
    finally:
        print("Hasta pronto.")


if __name__ == "__main__":
    main()