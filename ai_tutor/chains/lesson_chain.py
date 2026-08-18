import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def create_lesson_chain(llm):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, "prompts", "lesson_prompt.txt")
    
    with open(prompt_path, "r") as f:
        template = f.read()
    
    # Lesson chain returns text/markdown, NOT JSON
    prompt = PromptTemplate(
        input_variables=["topic", "level", "language"],
        template=template,
    )
    
    chain = prompt | llm | StrOutputParser()
    return chain
