"""
Run from the backend directory:

    python test_gemini_connection.py
"""

from app.services.llm import LLMService


def main() -> None:
    result = LLMService.generate_answer(
        user_message=(
            "What is the clearest action I can take to reduce my bill?"
        ),
        prompt_context=(
            "Household MAC001074 used 42.50 kWh during the latest week. "
            "The total estimated cost was £11.80. "
            "The cheapest period was 00:00 at 3.99 pence/kWh. "
            "The most expensive period was 18:00 at 67.20 pence/kWh. "
            "The current recommendation is to move electric vehicle charging "
            "from 18:00 to 00:00 for an estimated £2.28 saving. "
            "No abnormal usage was detected."
        ),
        history=[],
    )

    print("Model:", result["model"])
    print("Interaction ID:", result["response_id"])
    print("Answer:", result["answer"])


if __name__ == "__main__":
    main()