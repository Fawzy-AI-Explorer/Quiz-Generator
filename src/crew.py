"""Quiz Generator Crew Module"""
import os
import yaml
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
from src.config.config import OUTPUT_PATH
from src.Pydantic_models import Quiz, QuizAnalysisOutput, TrueFalseQuestions
from src.utils import create_output_dir


# Load agent configuration from YAML
try:
    with open(
        r'E:\DATA SCIENCE\projects\Agents\01-Quiz generator\src\config\agents.yaml',
        mode='r',
        encoding='utf-8'
    ) as file:
        agents_config = yaml.safe_load(file)
except Exception as e:
    raise RuntimeError(f"Failed to load agents.yaml: from {e}") from e

# Load task configuration from YAML
try:
    with open(
        r'E:\DATA SCIENCE\projects\Agents\01-Quiz generator\src\config\tasks.yaml',
        mode='r',
        encoding='utf-8'
    ) as file:
        tasks_config = yaml.safe_load(file)
except Exception as e:
    raise RuntimeError(f"Failed to load tasks.yaml: {e}") from e

load_dotenv()
PROVIDER = os.getenv("PROVIDER")
MODEL = os.getenv("MODEL")
BASE_URL = os.getenv("BASE_URL")
TEMPERATURE = float(os.getenv("TEMPERATURE"))

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
                api_key=os.getenv("GROQ_API_KEY")
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
            return [
                Task(
                name=tasks_config['quiz_generate']['name'],
                description=(
                    tasks_config["quiz_generate"]["description"]
                ),
                expected_output=(
                    tasks_config["quiz_generate"]["expected_output"]
                ),
                agent=self.mcq_generator_agent[0],
                output_file=tasks_config["quiz_generate"]["output_file"],
                output_json=Quiz
                ),
            Task(
                name=tasks_config['tf_question_task']['name'],
                description=(
                    tasks_config["tf_question_task"]["description"]
                ),
                expected_output=(
                    tasks_config["tf_question_task"]["expected_output"]
                ),
                agent=self.mcq_generator_agent[2],
                # context=tasks_config["quiz_analysis"]["context"],
                output_file=tasks_config["tf_question_task"]["output_file"],
                output_json=TrueFalseQuestions,
            ),
            Task(
                name=tasks_config['quiz_analysis']['name'],
                description=(
                    tasks_config["quiz_analysis"]["description"]
                ),
                expected_output=(
                    tasks_config["quiz_analysis"]["expected_output"]
                ),
                agent=self.mcq_generator_agent[1],
                # context=tasks_config["quiz_analysis"]["context"],
                output_file=tasks_config["quiz_analysis"]["output_file"],
                output_json=QuizAnalysisOutput,
            )
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
