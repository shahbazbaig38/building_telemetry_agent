from .database import execute_sql
from .sql_generation import generate_sql_from_nl, summarize_sql_result


# ---------- User-facing interactive helper ----------

def chat_with_agent():
    print("🏢 Building Telemetry AI Assistant (knowledge graph + safety)")
    print("Write natural language queries about building telemetry. Type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["quit", "exit", "bye", "goodbye"]:
                print("Assistant: Goodbye! Stay safe.")
                break

            sql = generate_sql_from_nl(user_input)
            print(f"--> Generated SQL: {sql}")
            result = execute_sql(sql)
            print(f"--> Result:\n{result}\n")

            explanation = summarize_sql_result(user_input, sql, result)
            print(f"--> Interpretation:\n{explanation}\n")

        except KeyboardInterrupt:
            print("\nAssistant: Session interrupted. Bye.")
            break
        except Exception as e:
            print(f"Assistant: Error: {str(e)}")


if __name__ == "__main__":
    chat_with_agent()