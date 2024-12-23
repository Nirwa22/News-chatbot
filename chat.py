from langchain import hub
prompt = hub.pull("hwchase17/react")
print(f"here is the prompt:{prompt}")
print(type(prompt.Action))