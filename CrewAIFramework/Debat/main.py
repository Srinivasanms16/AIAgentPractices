from crewai import Agent, Task, Crew, LLM
from CrewSetup import myCrew

crew = myCrew()
mycrew = crew.defineCrew()
result = mycrew.kickoff(inputs={'topic':'GST 2025 price reduction'})
print(result)





