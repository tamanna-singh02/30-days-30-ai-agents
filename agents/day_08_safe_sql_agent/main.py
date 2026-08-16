from agents.day_08_safe_sql_agent.agent.graph import graph
from agents.day_08_safe_sql_agent.ui import display_rich_output


def main():
    question = "Show me the top 10 customers by total order value."

    inputs = {"question": question, "max_retries": 3}
    final_state = graph.invoke(inputs)

    display_rich_output(final_state)


if __name__ == "__main__":
    main()