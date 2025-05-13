import os
import yaml
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
from src.config.config import OUTPUT_PATH
from src.Pydantic_models import Quiz, QuizAnalysisOutput
from src.utils import create_output_dir


# Load the YAML content
with open(
    r'E:\Data Science\Projects\crewai\Quiz-Generator\src\config\agents.yaml',
    mode='r',
    encoding='utf-8'
) as file:
    agents_config = yaml.safe_load(file)

with open(
    r'E:\Data Science\Projects\crewai\Quiz-Generator\src\config\tasks.yaml',
    mode='r',
    encoding='utf-8'
) as file:
    tasks_config = yaml.safe_load(file)


load_dotenv()
PROVIDER = os.getenv("PROVIDER")
MODEL = os.getenv("MODEL")
BASE_URL = os.getenv("BASE_URL")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))

class QuizGeneratorCrew:
    """Class to handle the quiz generation process using Crew AI """
    def __init__(self):

        create_output_dir(OUTPUT_PATH)
        self.llm = self._initialize_llm()
        self.mcq_generator_agent = self._initialize_agent()

    def _initialize_llm(self):
        """Initialize the LLM"""
        return LLM(
            # provider=PROVIDER,
            model='groq/gemma2-9b-it',
            # base_url="http://localhost:11434",
            temperature=0.5,
            api_key="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"
        )

    def _initialize_agent(self) -> list:
        """Initialize the MCQ generator agent"""
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
        )
        ]

    def _create_task(self) -> list:
        """Create a task for quiz generation.
        
        Returns:
            Task: A Task object configured for quiz generation with:
                - Description from tasks config
                - Expected output format
                - Associated MCQ generator agent
                - Output file path
                - Output JSON schema
        """
        return [
            Task(
            name=tasks_config['quiz_generator']['name'],
            description=(
                tasks_config["quiz_generator"]["description"]
            ),
            expected_output=(
                tasks_config["quiz_generator"]["expected_output"]
            ),
            agent=self.mcq_generator_agent[0],
            output_file=tasks_config["quiz_generator"]["output_file"],
            output_json=Quiz
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
    def kickoff(self, inputs):
        """Kickoff the quiz generation process.
        
        Args:
            inputs (dict): Dictionary containing input parameters.
                Required key:
                - text (str): The text content to generate quiz from
                
        Returns:
            dict: The generated quiz in JSON format
        """
        crew = Crew(
            agents=self.mcq_generator_agent,
            tasks=self._create_task(),
            process=Process.sequential,
            verbose=True
        )
        print("Crew initialized successfully!")
        return crew.kickoff(inputs=inputs)
