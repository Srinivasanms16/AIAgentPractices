from pydantic import BaseModel, Field
from crewai import Agent, Process, Task, Crew, LLM
from crewai.tools import tool
from dotenv import load_dotenv
import os
from serpapi import GoogleSearch

class Company(BaseModel):
    name:str = Field(description="name of company")
    reason:str = Field(description="Reason why we need invest in this company")


class StockPicker:
    def __init__(self):
        self.defineAgent()
        self.defineTask()

    
        
    @tool("Web_search")
    def webSearch(query:str) -> str:
        """ use this tool to do the web search.
            Its input parameter is, 
            query which of type string, it can be sector name or company name such as Banking Sector or IT Sector or SBI or TCS or TCS 2025 """
        key = os.getenv("SERPAPI_KEY")
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


    def defineAgent(self):
       #LLM
        openRouterModel = LLM(model="openrouter/tngtech/deepseek-r1t2-chimera:free",
                                 base_url="https://openrouter.ai/api/v1",
                                api_key=os.getenv("OPENROUTER_API_KEY"))
        
        openAIModel = LLM(model="openai/gpt-4.1-mini")
        
        self.Researcher = Agent(role="your a Senior Researcher",
                                goal="do reseach on {name} sector stocks for investment purpose",
                                backstory="your a Senior Researcher. Who will do web reseach on {name} sector stocks and rank the compaines",
                                tools=[self.webSearch],
                                llm=openAIModel,
                                )
        
        self.Analyzer = Agent(role ="your a Senior Analyzer",
                              goal="you analysis the report provided by reseacher",
                              backstory="your a Senior Analyzer. you analysis the report provided by reseacher. your analysis should helps to pick stocks for the investment ",
                              llm=openRouterModel)
        
        self.InvestmentBanker = Agent(role="your a Investment Banker",
                                 goal="your a Investment Banker who will start investing the amount to the top 2 stocks of {name} sector where will get the good returns and provide me the intraday tips",
                                 backstory="As the Investment banker you will check the financial report provided by Analyzer and start investing for both long term and intraday.",
                                 llm=openRouterModel)
        
        self.Manager= Agent(role="your a manger",
                            goal="your a manger who will manage this entire process. Who know what task has to delegated to which agent and when",
                            backstory="your a manger who will manage this entire process. Who know what task has to delegated to which agent and when",
                            llm=openRouterModel)
    
    def defineTask(self):
        self.listCompainesTask = Task(description="for {name} sector list the companies where we can invest",
                                  expected_output="your output should have proper information which helps analyzer to analysis.",
                                  agent=self.Researcher,
                                  output_file="output/company.md")
        
        self.analyzeTask = Task(description="Analysis the data provide by the Reseacher",
                                expected_output="generate the report which which will be used by investbanker for doing investment",
                                context=[self.listCompainesTask],
                                agent=self.Analyzer,
                                output_file="output/Analysis.md")
        
        self.invest = Task(description="we need to invest sum of $ {amount} for long term and list the companies for intraday",
                           expected_output="Analysis the report provided by the analyzer and start investing the sum of ${amount} to top 2 companies where will be good returns",
                           context=[self.analyzeTask],
                           agent=self.InvestmentBanker,
                           output_file="output/invest.md")
    
    def defineCrew(self):
        return Crew(agents=[self.Analyzer, self.Researcher, self.InvestmentBanker],
                    tasks=[ self.listCompainesTask,self.analyzeTask, self.invest],
                    process=Process.hierarchical,
                    manager_agent=self.Manager,
                    verbose=True
                    )
    



