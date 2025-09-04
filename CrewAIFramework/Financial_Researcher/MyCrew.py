from crewai import Agent, Task, Process, LLM, Crew
from crewai.tools import tool
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
from pydantic import BaseModel

class FinancialReseacher:
    def __init__(self):
        load_dotenv(override=True)
        self.creatAgent()
        self.createTask()

    @tool("web_search")
    def web_search(query: str) -> str:
        """Use this tool by passing query as company name example (SBI financial report 2025).
        Do NOT pass IDs, hashes, or task references.
        """
        print(f"term : {query}")
        key = os.getenv("SERPAPI_KEY")
        print(f"term : {key}")
        params = {
            "q": f"{query}",
            "location": "Austin, Texas, United States",
            "hl": "en",
            "gl": "us",
            "google_domain": "google.com",
            "api_key": key
                }
        search = GoogleSearch(params)
        results = search.get_dict()
        print(f"term : {str(results)}")
        return str(results)

    def creatAgent(self):
        #LLM
        openRouterModel = LLM(model="openrouter/tngtech/deepseek-r1t2-chimera:free",
                                 base_url="https://openrouter.ai/api/v1",
                                api_key=os.getenv("OPENROUTER_API_KEY"))
        
        openAIModel = LLM(model="openai/gpt-4.1-mini")
        
        #Researcher
        self.reseacherAgent = Agent(role="""your a senior reseacher. 
                                    Who will do research on the given {company} for the current financial year and provide the report""",
                                    goal="""your a senior reseacher. Who will do research on current Financial status,
                                      fund arrival, stock price of given {company} and provide the report """,
                                    backstory=""" your a senior reseacher. 
                                    Who will do the websearch and collect right information""",
                                    llm=openAIModel,
                                    tools=[self.web_search])
        
        #analysist
        self.analysistAgent = Agent(role="""your a senior Analsist""",
                                    goal="""your a senior analysis who will analysis the report provided by the researcher for the {company}
                                      and Create perfect bussiness report which gives information on wheather we can invest on the company or not""",
                                    backstory="""your a senior analysis who analyis the report 
                                    and create the bussiness report for the {company}""",
                                    LLM=openRouterModel)
        
    def createTask(self):
        self.reseacherTask = Task(description="""do financial reseach for the {company}'s quarterly results, annual earnings, 
                                  financial earnings, and stocks quarterly results etc for current financial year.""",
                                  expected_output="""do financial reseach for the {company}.
                                    Report generated will  helps us to take financial decision""",
                                  agent=self.reseacherAgent,
                                  output_file="output/research.md")
        
        self.reportTask = Task(description="""Analysis the report provided by the reseacher for the {company}. 
                               Generate bussiness report out it.""",
                               expected_output="""Analysis the Reseacher Report and Generate the Bussiness Report""",
                               agent=self.analysistAgent,
                               context=[self.reseacherTask],
                               output_file="output/Report.md")

    
    def defineCrew(self):
        return Crew(
            agents=[self.reseacherAgent, self.analysistAgent],
            tasks=[self.reseacherTask , self.reportTask],
            process=Process.sequential,
            verbose=True
            )

