from crewai import Agent, Task, Process, LLM, Crew
from MyCrew import FinancialReseacher

FReseacher = FinancialReseacher()
myCrew = FReseacher.defineCrew()

result = myCrew.kickoff({'company':'TCS'})

print(result)
