import os
from dotenv import load_dotenv
import logging
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import json
from services.llm_service import LLMService
from services.github_llm_service import GitHubLLMService
from services.document_service import DocumentService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"API Key loaded: {os.getenv('OPENAI_API_KEY')[:8]}...")  # Only log first 8 chars

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobDescription(BaseModel):
    text: str
    url: Optional[str] = None

@app.post("/generate")
async def generate_documents(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    model_provider: str = Form(...)
):
    try:
        # Log the incoming request
        logger.info(f"Received request with file: {resume.filename}")
        
        # Parse the job description JSON string
        job_desc_data = json.loads(job_description)
        job_desc = JobDescription(**job_desc_data)
        
        # Initialize services
        doc_service = DocumentService()
        
        # Select the appropriate LLM service
        if model_provider.lower() == "github":
            llm_service = GitHubLLMService()
        else:  # default to OpenAI
            llm_service = LLMService()
        
        # Process resume
        logger.info("Processing resume...")
        resume_content = await doc_service.process_resume(resume)
        logger.info(f"Resume processed, length: {len(resume_content)}")
        
        # Process job description
        job_desc_text = job_desc.text
        if job_desc.url:
            logger.info(f"Extracting job description from URL: {job_desc.url}")
            job_desc_text = await doc_service.extract_job_description(job_desc.url)
        logger.info(f"Job description processed, length: {len(job_desc_text)}")
        
        # Generate tailored documents
        logger.info(f"Generating documents using {model_provider}...")
        updated_resume = await llm_service.generate_tailored_resume(resume_content, job_desc_text)
        cover_letter = await llm_service.generate_cover_letter(resume_content, job_desc_text)
        
        return {
            "updated_resume": updated_resume,
            "cover_letter": cover_letter
        }
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 