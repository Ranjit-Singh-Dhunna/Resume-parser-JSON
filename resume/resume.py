import os
import json
import re
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import pdfplumber  

# Define the output schema (updated with links)
class PersonalInfo(BaseModel):
    full_name: str = Field(description="Full name")
    linkedin: Optional[str] = Field(default=None, description="LinkedIn URL")
    github: Optional[str] = Field(default=None, description="GitHub URL")
    portfolio: Optional[str] = Field(default=None, description="Portfolio/Website URL")

class Skills(BaseModel):
    categories: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Skill categories (e.g., 'Technical': ['Python'], 'Business': ['Financial Modeling']"
    )

class Experience(BaseModel):
    role: str = Field(description="Job title/position")
    company: str = Field(description="Organization name")
    duration: str = Field(description="Employment period")
    achievements: List[str] = Field(default=[], description="Quantifiable accomplishments")
    context: Optional[Dict[str, str]] = Field(
        default=None,
        description="Field-specific details (e.g., 'industry': 'Healthcare', 'tools': ['EPIC']"
    )

from typing import Dict, Optional, List
from pydantic import BaseModel, Field
from datetime import date

class Project(BaseModel):
    name: str = Field(..., description="Project name")
    domain: Optional[str] = Field(default=None, description="Field/industry (e.g., 'Finance', 'Healthcare IT')")
    components: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Relevant components by type (e.g., 'tools': ['Tableau'], 'methods': ['CRISP-DM']"
    )
    impact: Optional[str] = Field(default=None, description="Measurable outcomes")

class ResumeData(BaseModel):
    personal_info: PersonalInfo
    skills: Skills
    experience: List[Experience]
    projects: Optional[List[Project]] = Field(
        default=[],
        description="Detailed project information"
    )

# Initialize Ollama with a local model
llm = OllamaLLM(model="mistral")  # or "llama3", "phi3"

# Set up parser
parser = JsonOutputParser(pydantic_object=ResumeData)

# Extract text AND hyperlinks from PDF
def extract_text_and_links(pdf_path):
    text = ""
    links = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract text
            text += page.extract_text() + "\n"
            
            
            if hasattr(page, 'hyperlinks'):
                for link in page.hyperlinks:
                    if link:
                        links.append(link['uri'])
            
            # Alternative method for some PDFs
            if '/Annots' in page.objects:
                for annot in page.objects['/Annots']:
                    if annot.get('/A') and annot['/A'].get('/URI'):
                        links.append(annot['/A']['/URI'])
    
    # Extract link text and nearby text for context
    link_keywords = {
        'linkedin': ['linkedin', 'lnkd', 'li'],
        'github': ['github', 'gh'],
        'leetcode': ['leetcode', 'lc'],
        'portfolio': ['portfolio', 'website', 'personal site']
    }
    
    # Find text that looks like link labels
    for label in ['LinkedIn', 'GitHub', 'LeetCode', 'Portfolio']:
        if label in text:
            # Find the URL closest to this label
            nearby_text = text.split(label)[-1][:100]  # Get text after label
            url_match = re.search(r'https?://[^\s\)]+', nearby_text)
            if url_match:
                links.append(url_match.group())
    
    # Also get raw URLs
    raw_urls = re.findall(r'https?://[^\s\)]+', text)
    links.extend(raw_urls)
    
    # Deduplicate
    links = list(set(links))
    
    return text, links

# Modified prompt to include link hints
prompt = PromptTemplate(
    template="""
    Analyze this resume from an unknown field and extract structured data:

    RESUME TEXT:
    {resume_text}

    DETECTED LINKS:
    {hyperlinks}

    INSTRUCTIONS:
    1. FIELD DETECTION:
       - Identify the primary field (tech/business/healthcare/etc.) from content
       - Tag experiences/projects with 'domain' where obvious
    
    2. SKILLS:
       - Categorize skills automatically:
         - Technical (tools, programming)
         - Business (finance, management)
         - Clinical (for healthcare)
         - Creative (for design)
    
    3. EXPERIENCE:
       - Extract 1-2 key achievements per role
       - Add field context (e.g., "industry": "Biotech")
    
    4. PROJECTS:
       - Identify domain-specific components
       - Healthcare: protocols, regulations
       - Business: ROI, stakeholders
       - Tech: stack, algorithms

    {format_instructions}
    """,
    input_variables=["resume_text", "hyperlinks"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
# Run the pipeline
pdf_path = "resume.pdf"
if not os.path.exists(pdf_path):
    print(f"Error: Resume PDF file '{pdf_path}' not found.")
else:
    resume_text, hyperlinks = extract_text_and_links(pdf_path)
    chain = prompt | llm | parser

    try:
        result = chain.invoke({
            "resume_text": resume_text,
            "hyperlinks": hyperlinks  # Pass links to help the LLM
        })
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")