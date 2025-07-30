from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from mentormindflows.tools.writeFile_tool import WriteFileTool

@CrewBase
class CareerGuideCrew:
    agents_config = "config/careerguide_agents.yaml"
    tasks_config = "config/careerguide_tasks.yaml"

    ollama_llm = LLM(
        model='ollama/llama3.2:3b',
        base_url='http://localhost:11434',
    )

    @agent
    def career_matchmaker_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["career_matchmaker_agent"],
            llm=self.ollama_llm,
            verbose=True,
        )
    
    @agent
    def trend_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["trend_analyst_agent"],
            llm=self.ollama_llm,
            verbose=True,
        )
    
    @agent
    def future_planner_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["future_planner_agent"],
            llm=self.ollama_llm,
            verbose=True,
        )
    
    @task
    def match_careers_task(self) -> Task:
        return Task(
            config=self.tasks_config["match_careers_task"],
        )
    
    @task
    def validate_trends_task(self) -> Task:
        return Task(
            config=self.tasks_config["validate_trends_task"],
        )
    
    @task
    def build_roadmap_task(self) -> Task:
        return Task(
            config=self.tasks_config["build_roadmap_task"],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )