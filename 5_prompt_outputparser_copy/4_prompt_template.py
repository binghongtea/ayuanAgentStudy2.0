from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template(
    "请用通俗的语言解释 {concept} 的概念"
)
result = prompt_template.format(concept="大语言模型")
print(type(result)) # <class 'str'>
print(result)

# result = prompt_template.invoke(input={"concept": "大语言模型"})
# print(type(result)) # <class 'langchain_core.prompt_values.StringPromptValue'>
# print(result) # text='请用通俗的语言解释 大语言模型 的概念'
