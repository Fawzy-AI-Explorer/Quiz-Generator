"""Quiz Generator Crew Module"""
import os
import yaml
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
from src.config.config import OUTPUT_PATH
from src.Pydantic_models import Quiz, QuizAnalysisOutput, TrueFalseQuestions
from src.utils import create_output_dir

current_directory = os.path.dirname(os.path.abspath(__file__))
print(current_directory)
config_agent_path = '/mount/src/quiz-generator/src/config/agents.yaml'
config_task_path = '/mount/src/quiz-generator/src/config/tasks.yaml'
mcq_out_path = '/mount/src/quiz-generator/output/mcq_quiz.json'
tf_out_path = '/mount/src/quiz-generator/output/tf_quiz.json'
analyze_out_path = '/mount/src/quiz-generator/output/quiz_analyzer.json'

# Load agent configuration from YAML
try:
    with open(
        config_agent_path,
        mode='r',
        encoding='utf-8'
    ) as file:
        agents_config = yaml.safe_load(file)
except Exception as e:
    raise RuntimeError(f"Failed to load agents.yaml: from {e}") from e

# Load task configuration from YAML
try:
    with open(
        config_task_path,
        mode='r',
        encoding='utf-8'
    ) as file:
        tasks_config = yaml.safe_load(file)
except Exception as e:
    raise RuntimeError(f"Failed to load tasks.yaml: {e}") from e


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
            create_output_dir(OUTPUT_PATH)
            self.llm = self._initialize_llm()
            self.mcq_generator_agent = self._initialize_agent()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize QuizGeneratorCrew: {e}") from e

    def _initialize_llm(self):
        """
        Initialize the LLM
        
        Returns:
            LLM: Configured language model instance.
        """
        try:
            return LLM(
                # provider=PROVIDER,
                model='groq/gemma2-9b-it',
                # base_url="http://localhost:11434",
                temperature=1,
                api_key="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"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize LLM: {e}") from e

    def _initialize_agent(self) -> list:
        """
        Create and configure the agents used in the pipeline.

        Returns:
            list: A list containing the quiz generation and analysis agents.
        """
        try:
            return [
                Agent(
                role=agents_config["quiz_generator"]["role"],
                goal=agents_config["quiz_generator"]["goal"],
                backstory=(
                    agents_config["quiz_generator"]["backstory"]
                ),
                llm=self.llm,
                verbose=True,
                allow_delegation=False
            ),
            Agent(
                role=agents_config["quiz_analyzer"]["role"],
                goal=agents_config["quiz_analyzer"]["goal"],
                backstory=(
                    agents_config["quiz_analyzer"]["backstory"]
                ),
                llm=self.llm,
                verbose=True,
                allow_delegation=False
            ),
            Agent(
                role=agents_config["tf_question_agent"]["role"],
                goal=agents_config["tf_question_agent"]["goal"],
                backstory=(
                    agents_config["tf_question_agent"]["backstory"]
                ),
                llm=self.llm,
                verbose=True,
                allow_delegation=False
            )
            ]
        except Exception as e:
            raise RuntimeError(f"Failed to initialize agents: {e}") from e

    def _create_task(self) -> list:
        """Create a task for quiz generation.
        
        Returns:
            list: List of Task objects for quiz generation and analysis.
        """
        try:
            mcq_generate_task = Task(
                name=tasks_config['quiz_generate']['name'],
                description=(
                    tasks_config["quiz_generate"]["description"]
                ),
                expected_output=(
                    tasks_config["quiz_generate"]["expected_output"]
                ),
                agent=self.mcq_generator_agent[0],
                output_file=mcq_out_path,
                output_json=Quiz
                )
            tf_generate_task = Task(
                name=tasks_config['tf_question_task']['name'],
                description=(
                    tasks_config["tf_question_task"]["description"]
                ),
                expected_output=(
                    tasks_config["tf_question_task"]["expected_output"]
                ),
                agent=self.mcq_generator_agent[2],
                # context=tasks_config["quiz_analysis"]["context"],
                output_file=tf_out_path,
                output_json=TrueFalseQuestions,
            )
            analysis_generate_task = Task(
                name=tasks_config['quiz_analysis']['name'],
                description=(
                    tasks_config["quiz_analysis"]["description"]
                ),
                expected_output=(
                    tasks_config["quiz_analysis"]["expected_output"]
                ),
                agent=self.mcq_generator_agent[1],
                context=[mcq_generate_task, tf_generate_task],
                output_file=analyze_out_path,
                output_json=QuizAnalysisOutput,
            )
            return [
                mcq_generate_task,
                tf_generate_task,
                analysis_generate_task
            ]
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
                agents=self.mcq_generator_agent,
                tasks=self._create_task(),
                process=Process.sequential,
                verbose=True
            )
            print("Crew initialized successfully!")
            return crew.kickoff(inputs=inputs)
        except Exception as e:
            raise RuntimeError(f"Failed to kickoff crew: {e}") from e
