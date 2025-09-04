from crewai import Agent, Task, Crew, LLM, Process
from dotenv import load_dotenv
import os

class myCrew:

    def __init__(self):
        load_dotenv(override=True)
        self.defineAgent()
        self.defineTask()
    

    def defineAgent(self):
         myllm = LLM(model="openrouter/tngtech/deepseek-r1t2-chimera:free",
                    base_url="https://openrouter.ai/api/v1",
                    api_key=os.getenv("OPENROUTER_API_KEY"))
         
         self.debaterAgent = Agent(
            role="you are a debating agent",
            goal="when a {topic} is provided to you will debat on favour that {topic}",
            backstory="your are opposing agent, who is good in come up with relevant and precise points on the favour of the {topic}",
            llm= myllm,
            verbose=True,
        )
         self.opposeAgent = Agent(
            role="your are oppose agent will debat against the {topic}",
            goal="you are debating agent you will debat against the {topic} provide to you with relevant and precise points",
            backstory="your are opposing agent, who is good in come up with relevant and precise points against the {topic}",
            llm= myllm
        )
         self.judgeAgent = Agent(
            role="Decide the winner of the debate based on the arguments presented",
            goal="Given arguments for and against this topic: {topic}, decide which side is more convincing,based purely on the arguments presented.",
            backstory="""You are a fair judge with a reputation for weighing up arguments without factoring in 
                         your own views, and making a decision based purely on the merits of the argument.
                         The topic is: {topic}""",
            llm= myllm
        )

    def defineTask(self):
        self.proposeTask = Task(description="Debate on the favour of the {topic}",
                            expected_output="relevant and precise points",
                            agent=self.debaterAgent,
                            output_file="output/propose.md") 
        self.opposeTask = Task(description="Debat against {topic}",
                           expected_output="relevant and precise points",
                           agent=self.opposeAgent,
                           output_file="output/oppose.md") 
        self.decideTask = Task(description="Review the arguments presented by the debaters and decide which side is more convincing.",
                           expected_output="Your decision on which side is more convincing, and why.",
                           agent=self.judgeAgent,
                           output_file="output/decide.md")
        
    def defineCrew(self):
        return Crew(agents=[self.debaterAgent, self.opposeAgent, self.judgeAgent],
                    tasks=[self.proposeTask,self.opposeTask,self.decideTask],
                    process=Process.sequential,
                    verbose=True)
    


    
      
         
       

  




