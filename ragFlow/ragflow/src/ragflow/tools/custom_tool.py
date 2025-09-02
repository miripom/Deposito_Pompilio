"""Custom tools for Ragflow.

This module provides custom tool functions for use with CrewAI agents,
including a web search tool that leverages DuckDuckGo via the ``ddgs`` library.

Functions:
    search_web(query: str) -> str: Performs a web search and returns formatted results.
"""

from crewai.tools import tool  # pylint: disable=import-error
from ddgs import DDGS  # pylint: disable=import-error

@tool
def search_web(query: str) -> str:
    """
    Performs a web search using DuckDuckGo and returns the top 3 results.

    Args:
        query (str): The search query to send to DuckDuckGo.

    Returns:
        str: A formatted string containing the top 3 search results, or an error message
            or a message indicating no results were found.

    Example:
        >>> search_web("Python programming")
        "Risultati della ricerca per 'Python programming':\n
        RISULTATO 1:
        Titolo: Python - Official Site
        URL: https://www.python.org/
        Descrizione: The official home of the Python Programming Language.
        ----------------------------------------"

    Raises:
        OSError: If there is a problem with the network or DuckDuckGo service.
        TimeoutError: If the search times out.
        ValueError: If the query is invalid or another error occurs.
    """
    try:
        with DDGS(verify=False) as ddgs:
            risultati = list(
                ddgs.text(
                    query,
                    region="it-it",
                    safesearch="off",
                    max_results=3,
                )
            )

        if not risultati:
            return f"Nessun risultato trovato per la query: {query}"

        lines = [f"Risultati della ricerca per '{query}':\n"]
        for index, result in enumerate(risultati, 1):
            titolo = result.get("title", "Senza titolo")
            url = result.get("href") or result.get("url") or "URL non disponibile"
            snippet = result.get("body", "Nessuna descrizione disponibile")
            lines.append(
                "\n".join(
                    [
                        f"RISULTATO {index}:",
                        f"Titolo: {titolo}",
                        f"URL: {url}",
                        f"Descrizione: {snippet}",
                        "-" * 40,
                        "",
                    ]
                )
            )

        return "".join(lines)
    except (OSError, TimeoutError, ValueError) as exc:
        return f"Errore durante la ricerca: {exc}"
