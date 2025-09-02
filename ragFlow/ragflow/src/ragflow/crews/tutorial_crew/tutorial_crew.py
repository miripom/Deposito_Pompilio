"""Crew per la creazione di tutorial e spiegazioni strutturate.

Definisce `TutorialCrew`, che coordina agenti e task per pianificare, redigere
e compilare tutorial completi in modo sequenziale.
"""

from typing import List

from crewai import Agent, Crew, Process, Task  # pylint: disable=import-error
from crewai.project import CrewBase, agent, crew, task  # pylint: disable=import-error
from crewai.agents.agent_builder.base_agent import BaseAgent  # pylint: disable=import-error


@CrewBase
class TutorialCrew():
    """Crew per creare tutorial e spiegazioni dettagliate.

    Attributi:
        agents (List[BaseAgent]): Lista degli agenti utilizzati dalla crew.
        tasks (List[Task]): Lista dei task assegnati alla crew.
    """

    agents: List[BaseAgent]
    tasks: List[Task]
    # Iniettati dal decoratore CrewBase via configurazioni YAML
    agents_config: dict
    tasks_config: dict

    @agent
    def tutorial_manager(self) -> Agent:
        """Crea l'agente tutorial_manager.

        Returns:
            Agent: Un agente configurato come tutorial manager.
        """
        return Agent(
            config=self.agents_config['tutorial_manager'],
            verbose=True,
            allow_delegation=True
        )

    @agent
    def content_writer_1(self) -> Agent:
        """Crea l'agente content_writer_1.

        Returns:
            Agent: Un agente configurato come primo scrittore di contenuti.
        """
        return Agent(
            config=self.agents_config['content_writer_1'],
            verbose=True
        )

    @agent
    def content_writer_2(self) -> Agent:
        """Crea l'agente content_writer_2.

        Returns:
            Agent: Un agente configurato come secondo scrittore di contenuti.
        """
        return Agent(
            config=self.agents_config['content_writer_2'],
            verbose=True
        )

    @task
    def plan_tutorial(self) -> Task:
        """Crea il task per pianificare il tutorial.

        Returns:
            Task: Un task per la pianificazione del tutorial.
        """
        return Task(
            config=self.tasks_config['plan_tutorial'],
            agent=self.tutorial_manager()
        )

    @task
    def write_introduction(self) -> Task:
        """Crea il task per scrivere l'introduzione.

        Returns:
            Task: Un task per la scrittura dell'introduzione.
        """
        return Task(
            config=self.tasks_config['write_introduction'],
            agent=self.content_writer_1()
        )

    @task
    def write_main_content(self) -> Task:
        """Crea il task per scrivere il contenuto principale.

        Returns:
            Task: Un task per la scrittura del contenuto principale.
        """
        return Task(
            config=self.tasks_config['write_main_content'],
            agent=self.content_writer_2()
        )

    @task
    def compile_final(self) -> Task:
        """Crea il task per compilare il tutorial finale.

        Returns:
            Task: Un task per la compilazione finale del tutorial, che utilizza
            il contesto dei task precedenti.
        """
        return Task(
            config=self.tasks_config['compile_final'],
            agent=self.tutorial_manager(),
            context=[
                self.plan_tutorial(),
                self.write_introduction(),
                self.write_main_content()
            ]
        )

    @crew
    def crew(self) -> Crew:
        """Crea e restituisce la crew TutorialCrew.

        Returns:
            Crew: La crew configurata per la creazione di tutorial in modo sequenziale.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
            process=Process.sequential,
        )