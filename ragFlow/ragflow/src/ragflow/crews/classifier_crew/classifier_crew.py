"""Crew di classificazione a due livelli per domande utente.

Questo modulo definisce la classe `ClassifierCrew`, che utilizza agenti e
task per determinare se una domanda è di matematica e, in caso negativo,
classificarne il dominio.
"""

from typing import List

from crewai import Agent, Crew, Process, Task  # pylint: disable=import-error
from crewai.project import CrewBase, agent, crew, task  # pylint: disable=import-error
from crewai.agents.agent_builder.base_agent import BaseAgent  # pylint: disable=import-error

@CrewBase
class ClassifierCrew():
    """Crew per classificare il dominio delle domande utente a due livelli.

    Attributes:
        agents (List[BaseAgent]): List of agents used in the crew.
        tasks (List[Task]): List of tasks to be performed by the crew.
    """

    agents: List[BaseAgent]
    tasks: List[Task]
    # Questi attributi vengono iniettati dal decoratore CrewBase tramite configurazioni YAML
    agents_config: dict
    tasks_config: dict

    @agent
    def math_detector(self) -> Agent:
        """Creates the math detector agent.

        Returns:
            Agent: An agent configured to detect math-related questions.
        """
        return Agent(
            config=self.agents_config['math_detector'],
            verbose=True
        )

    @agent
    def domain_classifier(self) -> Agent:
        """Creates the domain classifier agent.

        Returns:
            Agent: An agent configured to classify the domain of non-math questions.
        """
        return Agent(
            config=self.agents_config['domain_classifier'],
            verbose=True
        )

    @task
    def detect_math_task(self) -> Task:
        """Creates the task for detecting math questions.

        Returns:
            Task: A task for identifying whether a question is math-related.
        """
        return Task(
            config=self.tasks_config['detect_math_task']
        )

    @task
    def classify_nonmath_domain_task(self) -> Task:
        """Creates the task for classifying non-math domains.

        Returns:
            Task: A task for classifying the domain of non-math questions.
        """
        return Task(
            config=self.tasks_config['classify_nonmath_domain_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the two-level classifier crew.

        Returns:
            Crew: The crew object with agents and tasks set up for classification.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
