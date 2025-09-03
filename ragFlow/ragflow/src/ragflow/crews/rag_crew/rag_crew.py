"""Crew per ricerche RAG mediche locali.

Questo modulo definisce `RagCrew`, una classe responsabile di orchestrare un agente 
specialista medico e i relativi task per eseguire ricerche su un indice RAG locale.
La crew è specializzata nell'analisi di documenti medici e nella risposta a query
attraverso il sistema di Retrieval-Augmented Generation.

Example:
    Utilizzo base di RagCrew:
    
    >>> from ragflow.crews.rag_crew.rag_crew import RagCrew
    >>> crew = RagCrew()
    >>> agent = crew.medical_specialist()
    >>> task = crew.rag_search_task()
    >>> rag_crew = crew.crew()
    >>> # Utilizza la crew per eseguire ricerche RAG mediche
"""

from typing import List

from crewai import Agent, Crew, Process, Task  # pylint: disable=import-error
from crewai.project import CrewBase, agent, crew, task  # pylint: disable=import-error
from crewai.agents.agent_builder.base_agent import BaseAgent  # pylint: disable=import-error
from ragflow.tools.rag_tool import medical_search_tool

@CrewBase
class RagCrew():
    """Crew per eseguire ricerche nel RAG medico locale.

    Questa classe coordina agenti specializzati per la ricerca medica e task
    per l'interrogazione di un sistema RAG locale. Utilizza CrewAI per orchestrare
    il processo di ricerca semantica su documenti medici indicizzati tramite FAISS.

    Attributes:
        agents (List[BaseAgent]): Lista degli agenti utilizzati dalla crew.
        tasks (List[Task]): Lista dei task assegnati alla crew.
        agents_config (dict): Configurazione degli agenti caricata da YAML.
        tasks_config (dict): Configurazione dei task caricata da YAML.

    Example:
        >>> crew = RagCrew()
        >>> medical_crew = crew.crew()
        >>> # Esegui ricerca RAG medica
        >>> result = medical_crew.kickoff(inputs={"query": "sintomi dell'ipertensione"})
    """

    agents: List[BaseAgent]
    tasks: List[Task]
    # Iniettati dal decoratore CrewBase via configurazioni YAML
    agents_config: dict
    tasks_config: dict

    @agent
    def medical_specialist(self) -> Agent:
        """Crea l'agente specialista medico per la ricerca RAG.

        Questo metodo crea e configura un agente specializzato nella ricerca medica
        utilizzando la configurazione definita nei file YAML. L'agente è equipaggiato
        con il tool medical_search_tool per interrogare il database medico Qdrant.

        Returns:
            Agent: Un agente configurato per eseguire ricerche mediche tramite RAG.
                  L'agente include il tool medical_search_tool e modalità verbose attiva.

        Raises:
            KeyError: Se la configurazione 'medical_specialist' non è presente
                     in agents_config.
            ValueError: Se la configurazione dell'agente non è valida.
            RuntimeError: Se il sistema RAG non è inizializzato correttamente.

        Example:
            >>> crew = RagCrew()
            >>> agent = crew.medical_specialist()
            >>> isinstance(agent, Agent)
            True
            >>> agent.verbose
            True
        """
        return Agent(
            config=self.agents_config['medical_specialist'],
            tools=[medical_search_tool],
            verbose=True
        )

    @task
    def rag_search_task(self) -> Task:
        """Crea il task di ricerca RAG.

        Questo metodo crea e configura un task per la ricerca semantica nel sistema RAG
        medico utilizzando la configurazione definita nei file YAML. Il task è ottimizzato
        per interrogazioni su documenti medici indicizzati.

        Returns:
            Task: Un task configurato per la ricerca nel sistema RAG medico.
                 Il task utilizza la configurazione definita in tasks_config
                 e può eseguire ricerche semantiche su documenti medici.

        Raises:
            KeyError: Se la configurazione 'rag_search_task' non è presente
                     in tasks_config.
            ValueError: Se la configurazione del task non è valida.
            RuntimeError: Se il sistema RAG non è inizializzato correttamente.

        Example:
            >>> crew = RagCrew()
            >>> task = crew.rag_search_task()
            >>> isinstance(task, Task)
            True
        """
        return Task(
            config=self.tasks_config['rag_search_task']
        )

    @crew
    def crew(self) -> Crew:
        """Crea e restituisce la crew RAG.

        Questo metodo assembla gli agenti specializzati e i task in una crew funzionale
        che esegue il processo di ricerca RAG medica in modalità sequenziale.
        La crew è ottimizzata per la ricerca semantica su documenti medici.

        Returns:
            Crew: La crew configurata per eseguire ricerche RAG in modo sequenziale.
                 Include tutti gli agenti e task definiti nella classe con modalità
                 verbose attiva per il debugging delle operazioni RAG.

        Raises:
            ValueError: Se gli agenti o i task non sono configurati correttamente.
            TypeError: Se il tipo di processo non è supportato.
            RuntimeError: Se l'indice RAG non è disponibile o corrotto.

        Example:
            >>> crew = RagCrew()
            >>> rag_crew = crew.crew()
            >>> isinstance(rag_crew, Crew)
            True
            >>> rag_crew.process == Process.sequential
            True
            >>> rag_crew.verbose
            True
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
