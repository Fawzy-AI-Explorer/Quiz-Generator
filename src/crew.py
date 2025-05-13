from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
from src.config.config import OUTPUT_PATH
from Pydantic_models import Quiz
import os

import yaml

# Load the YAML content
with open(r'E:\DATA SCIENCE\projects\Agents\01-Quiz generator\src\config\agents.yaml', 'r') as file:
    agents_config = yaml.safe_load(file)
    # print(config["quiz_generator"])

with open(r'E:\DATA SCIENCE\projects\Agents\01-Quiz generator\src\config\tasks.yaml', 'r') as file:
    tasks_config = yaml.safe_load(file)
    # print(config["quiz_generator"])


load_dotenv()
PROVIDER = os.getenv("PROVIDER")
MODEL = os.getenv("MODEL")
BASE_URL = os.getenv("BASE_URL")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))

class QuizGeneratorCrew:
    """Class to handle the quiz generation process using Crew AI """
    def __init__(self):
        
        os.makedirs(OUTPUT_PATH, exist_ok=True)
        self.llm = self._initialize_llm()
        self.mcq_generator_agent = self._initialize_agent()

    def _initialize_llm(self):
        """Initialize the LLM"""
        return LLM(
            provider=PROVIDER,
            model=MODEL,
            base_url="http://localhost:11434",
            temperature=TEMPERATURE
        )

    def _initialize_agent(self):
        """Initialize the MCQ generator agent"""
        # return Agent(
        #     role="Senior Educational Content Designer",
        #     goal="Create high-quality MCQs from educational content",
        #     backstory=(
        #         "You are an expert in educational MCQs creation with "
        #         "specialization in Quiz design and pedagogy. "
        #         "Skilled at creating multiple-choice questions "
        #         "that test conceptual understanding."
        #     ),
        #     llm=self.llm,
        #     verbose=True,
        #     allow_delegation=False
        # )
        return Agent(
            role=agents_config["quiz_generator"]["role"],
            goal=agents_config["quiz_generator"]["goal"],
            backstory=(
                agents_config["quiz_generator"]["backstory"]
            ),
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    


    def _create_task(self):
        # return Task(
        # description=(
        #     "\n".join([
        #         "Analyze the following technical content and generate a high-quality quiz:",
        #         "CONTENT: ",
        #         "{text}",
        #         "REQUIREMENTS: ",
        #         "1. Generate exactly 10 MCQs covering key concepts",
        #         "2. Ensure questions progress from basic to advanced",
        #         "3. Each question must have:",
        #         "- Clear question with complete phrasing",
        #         "- 4 plausible distractors",
        #         "- One unambiguous correct answer",
                
        #         "- Output strict JSON format"                   
        #             ])
        # ),
        # expected_output=(
        #     "JSON object containing 10 MCQs following the specified format. "
        #     "Ensure proper escaping for JSON validity."
        # ),
        # agent=self.mcq_generator_agent,
        # output_file=os.path.join(OUTPUT_PATH, "generated_quiz.json"),
        # output_json=Quiz
        # )
        return Task(
            description=(
                tasks_config["quiz_generator"]["description"]
            ),
            expected_output=(
                tasks_config["quiz_generator"]["expected_output"]
            ),
            agent=self.mcq_generator_agent,
            output_file=tasks_config["quiz_generator"]["output_file"],
            output_json=Quiz
        )
    def kickoff(self, inputs):

        crew = Crew(
            agents=[self.mcq_generator_agent],
            tasks=[self._create_task()],
            process=Process.sequential
        )
        print("Crew initialized successfully!")
        return crew.kickoff(inputs=inputs)
    


