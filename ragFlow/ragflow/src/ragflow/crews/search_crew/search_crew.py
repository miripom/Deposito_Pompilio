"""Crew per ricerche web e sintesi dei risultati.

Questo modulo definisce `SearchCrew`, una classe che coordina un agente di ricerca web
e i task correlati per produrre riassunti strutturati dei contenuti trovati online.

Example:
    Utilizzo base di SearchCrew:
    
    >>> from ragflow.crews.search_crew.search_crew import SearchCrew
    >>> crew = SearchCrew()
    >>> agent = crew.web_research_specialist()
    >>> task = crew.search_and_summarize_task()
    >>> search_crew = crew.crew()
    >>> # Utilizza la crew per eseguire ricerche web
"""

from typing import List

from crewai import Agent, Crew, Process, Task  # pylint: disable=import-error
from crewai.project import CrewBase, agent, crew, task  # pylint: disable=import-error
from crewai.agents.agent_builder.base_agent import BaseAgent  # pylint: disable=import-error
from ragflow.tools.custom_tool import search_web  # pylint: disable=import-error

@CrewBase
class SearchCrew():
    """Crew per eseguire ricerche web e creare riassunti.

    Questa classe coordina agenti specializzati per la ricerca web e task
    per la sintesi dei contenuti. Utilizza CrewAI per orchestrare il processo
    di ricerca e generazione di riassunti strutturati.

    Attributes:
        agents (List[BaseAgent]): Lista degli agenti utilizzati dalla crew.
        tasks (List[Task]): Lista dei task assegnati alla crew.
        agents_config (dict): Configurazione degli agenti caricata da YAML.
        tasks_config (dict): Configurazione dei task caricata da YAML.

    Example:
        >>> crew = SearchCrew()
        >>> web_crew = crew.crew()
        >>> # Esegui ricerca e sintesi
        >>> result = web_crew.kickoff(inputs={"topic": "intelligenza artificiale"})
    """

    agents: List[BaseAgent]
    tasks: List[Task]
    # Iniettati dal decoratore CrewBase via configurazioni YAML
    agents_config: dict
    tasks_config: dict

    @agent
    def web_research_specialist(self) -> Agent:
        """Crea l'agente specialista per la ricerca web.

        Questo metodo crea e configura un agente specializzato nella ricerca web
        utilizzando la configurazione definita nei file YAML. L'agente è equipaggiato
        con strumenti di ricerca web personalizzati.

        Returns:
            Agent: Un agente configurato per eseguire ricerche web e generare riassunti.
                  L'agente include il tool search_web e modalità verbose attiva.

        Raises:
            KeyError: Se la configurazione 'web_research_specialist' non è presente
                     in agents_config.
            ValueError: Se la configurazione dell'agente non è valida.

        Example:
            >>> crew = SearchCrew()
            >>> agent = crew.web_research_specialist()
            >>> isinstance(agent, Agent)
            True
            >>> agent.verbose
            True
        """
        return Agent(
            config=self.agents_config['web_research_specialist'],
            tools=[search_web],
            verbose=True
        )

    @task
    def search_and_summarize_task(self) -> Task:
        """Crea il task di ricerca e sintesi.

        Questo metodo crea e configura un task per la ricerca web e la sintesi
        dei risultati utilizzando la configurazione definita nei file YAML.

        Returns:
            Task: Un task configurato per la ricerca web e la creazione di riassunti.
                 Il task utilizza la configurazione definita in tasks_config.

        Raises:
            KeyError: Se la configurazione 'search_and_summarize_task' non è presente
                     in tasks_config.
            ValueError: Se la configurazione del task non è valida.

        Example:
            >>> crew = SearchCrew()
            >>> task = crew.search_and_summarize_task()
            >>> isinstance(task, Task)
            True
        """
        return Task(
            config=self.tasks_config['search_and_summarize_task']
        )

    @crew
    def crew(self) -> Crew:
        """Crea e restituisce la crew per la ricerca web e la sintesi.

        Questo metodo assembla gli agenti e i task in una crew funzionale
        che esegue il processo di ricerca web e sintesi in modalità sequenziale.

        Returns:
            Crew: La crew configurata per eseguire ricerche web e generare
                 riassunti in modo sequenziale. Include tutti gli agenti e task
                 definiti nella classe con modalità verbose attiva.

        Raises:
            ValueError: Se gli agenti o i task non sono configurati correttamente.
            TypeError: Se il tipo di processo non è supportato.

        Example:
            >>> crew = SearchCrew()
            >>> web_crew = crew.crew()
            >>> isinstance(web_crew, Crew)
            True
            >>> web_crew.process == Process.sequential
            True
            >>> web_crew.verbose
            True
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
