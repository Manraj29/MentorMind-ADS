from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class Mentormind():
    """Mentormind crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # @agent
    # def preprocessing_agent(self) -> Agent:
    #     return Agent(config=self.agents_config['preprocessing_agent'], verbose=True)

    @agent
    def risk_classification_agent(self) -> Agent:
        return Agent(config=self.agents_config['risk_classification_agent'], verbose=True)

    @agent
    def recommendation_agent(self) -> Agent:
        return Agent(config=self.agents_config['recommendation_agent'], verbose=True)

    @agent
    def eda_agent(self) -> Agent:
        return Agent(config=self.agents_config['eda_agent'], verbose=True)

    # @agent
    # def study_planner_agent(self) -> Agent:
    #     return Agent(config=self.agents_config['study_planner_agent'], verbose=True)

    # @agent
    # def career_guide_agent(self) -> Agent:
    #     return Agent(config=self.agents_config['career_guide_agent'], verbose=True)

    # @agent
    # def peer_comparison_agent(self) -> Agent:
    #     return Agent(config=self.agents_config['peer_comparison_agent'], verbose=True)

    # @agent
    # def attendance_risk_agent(self) -> Agent:
    #     return Agent(config=self.agents_config['attendance_risk_agent'], verbose=True)

    # @task
    # def preprocessing_task(self) -> Task:
    #     return Task(config=self.tasks_config['preprocessing_task'])

    @task
    def risk_classification_task(self) -> Task:
        return Task(config=self.tasks_config['risk_classification_task'])

    @task
    def recommendation_task(self) -> Task:
        return Task(config=self.tasks_config['recommendation_task'])

    @task
    def eda_task(self) -> Task:
        return Task(config=self.tasks_config['reporting_task'])

    # @task
    # def study_planner_task(self) -> Task:
    #     return Task(config=self.tasks_config['study_planner_task'])

    # @task
    # def career_guide_task(self) -> Task:
    #     return Task(config=self.tasks_config['career_guide_task'])

    # @task
    # def peer_comparison_task(self) -> Task:
    #     return Task(config=self.tasks_config['peer_comparison_task'])

    # @task
    # def attendance_risk_task(self) -> Task:
    #     return Task(config=self.tasks_config['attendance_risk_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,  # You can switch to hierarchical if needed
            verbose=True
        )
    
    @task
    def reporting_task(self) -> Task:
        task = Task(
            config=self.tasks_config['reporting_task'],
            output_file='report.md'  # Don't save to file for now; we will return the result as output
        )
        return task

