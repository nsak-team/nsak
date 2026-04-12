from langchain.tools import tool


@tool  # type: ignore[misc]
def human_interaction_hook(question: str) -> str:
    """
    Ask the human operator a question and return their answer.

    Use this tool when you need information, confirmation, or guidance that
    cannot be determined from the available tools or the current context.

    Args:
        question: The question or request to present to the human operator.

    Returns
    -------
        The human operator's response as a string.
    """
    return input(f"[Human Input Required]\n{question}\n> ")
