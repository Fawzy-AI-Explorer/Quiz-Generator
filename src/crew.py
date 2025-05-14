"""Quiz Generator Crew Module"""

import os
import yaml
from crewai import Agent, Task, Crew, Process, LLM
from config.config import OUTPUT_PATH
from src.pydantic_models import MCQQuiz, QuizAnalysisOutput, TrueFalseQuiz
from src.utils import create_output_dir


class QuizGeneratorCrew:
    """
    Class to handle the quiz generation process using Crew AI

     This class sets up the agents and tasks required for:
    1. Generating MCQs from technical content.
    2. Analyzing the quality of generated MCQs.
    """

    def __init__(self):
        """Initialize the QuizGeneratorCrew class."""
        try:
            create_output_dir()
            self.agents_config, self.tasks_config = self._load_config()
            self.llm = self._initialize_llm()
            self.agents = self._initialize_agents(self.agents_config)
            self.tasks = self._initialize_tasks(self.tasks_config)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize QuizGeneratorCrew: {e}") from e

    def _load_config(self):
        # Load agent configuration from YAML
        try:
            with open(file="config/agents.yaml", mode="r", encoding="utf-8") as file:
                agents_config = yaml.safe_load(file)
        except Exception as e:
            raise RuntimeError(f"Failed to load agents.yaml: from {e}") from e

        # Load task configuration from YAML
        try:
            with open(file="config/tasks.yaml", mode="r", encoding="utf-8") as file:
                tasks_config = yaml.safe_load(file)
        except Exception as e:
            raise RuntimeError(f"Failed to load tasks.yaml: {e}") from e

        return agents_config, tasks_config

    def _initialize_llm(self):
        """
        Initialize the LLM

        Returns:
            LLM: Configured language model instance.
        """
        try:
            return LLM(
                # provider=PROVIDER,
                model=os.getenv("MODEL"),
                # base_url="http://localhost:11434",
                temperature=float(os.getenv("TEMPERATURE")),
                api_key=os.getenv("GROQ_API_KEY"),
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize LLM: {e}") from e

    def _initialize_agents(self, config) -> list:
        """
        Create and configure the agents used in the pipeline.

        Returns:
            list: A list containing the quiz generation and analysis agents.
        """
        try:
            return [
                Agent(
                    role=config["quiz_generator"]["role"],
                    goal=config["quiz_generator"]["goal"],
                    backstory=(config["quiz_generator"]["backstory"]),
                    llm=self.llm,
                    verbose=True,
                    allow_delegation=False,
                ),
                Agent(
                    role=config["quiz_analyzer"]["role"],
                    goal=config["quiz_analyzer"]["goal"],
                    backstory=(config["quiz_analyzer"]["backstory"]),
                    llm=self.llm,
                    verbose=True,
                    allow_delegation=False,
                ),
                Agent(
                    role=config["tf_question_agent"]["role"],
                    goal=config["tf_question_agent"]["goal"],
                    backstory=(config["tf_question_agent"]["backstory"]),
                    llm=self.llm,
                    verbose=True,
                    allow_delegation=False,
                ),
            ]
        except Exception as e:
            raise RuntimeError(f"Failed to initialize agents: {e}") from e

    def _initialize_tasks(self, config) -> list:
        """Create a task for quiz generation.

        Returns:
            list: List of Task objects for quiz generation and analysis.
        """
        try:
            mcq_generate_task = Task(
                name=config["quiz_generate"]["name"],
                description=(config["quiz_generate"]["description"]),
                expected_output=(config["quiz_generate"]["expected_output"]),
                agent=self.agents[0],
                output_file=os.path.join(OUTPUT_PATH, "mcq_quiz.json"),
                output_json=MCQQuiz,
            )
            tf_generate_task = Task(
                name=config["tf_question_task"]["name"],
                description=(config["tf_question_task"]["description"]),
                expected_output=(config["tf_question_task"]["expected_output"]),
                agent=self.agents[2],
                output_file=os.path.join(OUTPUT_PATH, "tf_quiz.json"),
                output_json=TrueFalseQuiz,
                # async_execution=True
            )
            analysis_generate_task = Task(
                name=config["quiz_analysis"]["name"],
                description=(config["quiz_analysis"]["description"]),
                expected_output=(config["quiz_analysis"]["expected_output"]),
                agent=self.agents[1],
                context=[mcq_generate_task, tf_generate_task],
                output_file=os.path.join(OUTPUT_PATH, "quiz_analysis.json"),
                output_json=QuizAnalysisOutput,
            )
            return [mcq_generate_task, tf_generate_task, analysis_generate_task]
        except Exception as e:
            raise RuntimeError(f"Failed to create tasks: {e}") from e

    def kickoff(self, inputs):
        """Kickoff the quiz generation process.

        Args:
            inputs (dict): Dictionary containing input parameters.
                Required key:
                - text (str): The text content to generate quiz from

        Returns:
            dict: The generated quiz in JSON format
        """
        try:
            crew = Crew(
                agents=self.agents,
                tasks=self.tasks,
                process=Process.sequential,
                verbose=True,
            )
            print("Crew initialized successfully!")
            return crew.kickoff(inputs=inputs)
        except Exception as e:
            raise RuntimeError(f"Failed to kickoff crew: {e}") from e
