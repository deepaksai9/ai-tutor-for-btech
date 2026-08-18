import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def create_learning_path_chain(llm):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, "prompts", "learning_path_prompt.txt")
    
    with open(prompt_path, "r") as f:
        template = f.read()
        
    parser = JsonOutputParser()

    prompt = PromptTemplate(
        input_variables=["level", "language"],
        template=template + "\n\n{format_instructions}\nReturn only the JSON object.",
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = prompt | llm | parser
    return chain
