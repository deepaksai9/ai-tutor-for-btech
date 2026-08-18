import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List

# Define data structure
class AssessmentResult(BaseModel):
    level: str = Field(description="User level: Beginner, Intermediate, or Advanced")
    strengths: List[str] = Field(description="List of user strengths")
    weaknesses: List[str] = Field(description="List of user weaknesses")

def create_assessment_chain(llm):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, "prompts", "assessment_prompt.txt")
    
    with open(prompt_path, "r") as f:
        template_content = f.read()
    
    parser = JsonOutputParser(pydantic_object=AssessmentResult)

    prompt = PromptTemplate(
        input_variables=["user_answers", "language"],
        template=template_content + "\n\n{format_instructions}\nMake sure to return ONLY the JSON object and no other text.",
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = prompt | llm | parser
    return chain
