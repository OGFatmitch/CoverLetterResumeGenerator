import os
from openai import OpenAI
from dotenv import load_dotenv
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the project root directory (two levels up from this file)
project_root = Path(__file__).parent.parent.parent
env_path = project_root / '.env'

# Load environment variables
load_dotenv(dotenv_path=env_path, override=True)  # Add override=True to ensure .env takes precedence

# Explicitly get the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key or not api_key.startswith("sk-"):
    raise ValueError("Invalid or missing OpenAI API key in .env file")

logger.info(f"Loading .env from: {env_path}")
logger.info(f"API Key loaded: {api_key[:8]}...")

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=api_key)
    
    async def generate_tailored_resume(self, resume_content: str, job_description: str) -> str:
        prompt = f"""You are an expert resume strategist and hiring consultant with deep experience in optimizing resumes for maximum impact. Your task is to enhance the candidate's resume to perfectly align with the target role while maintaining authenticity and demonstrating clear value.

ANALYSIS PHASE:
1. Job Requirements Analysis:
   - Identify the 4-5 most critical requirements from the job description
   - Note any specific technologies, methodologies, or skills mentioned
   - Identify key industry terms and buzzwords
   - Understand the role's scope and impact expectations

2. Resume Content Analysis:
   - Review current experience and achievements
   - Identify transferable skills and relevant projects
   - Note any gaps in required skills or experience
   - Identify opportunities for better alignment

3. Strategic Enhancement Opportunities:
   - Identify areas where experience can be better aligned
   - Note opportunities to emphasize relevant achievements
   - Consider how to better demonstrate impact
   - Identify ways to incorporate industry-specific language

BULLET POINT STRUCTURE:
Each bullet point should follow this comprehensive structure:
1. Action (What was done):
   - Clear, specific action verb
   - Detailed description of the task or project
   - Scope and scale of the work
   - Technologies or methodologies used

2. Method (How it was done):
   - Specific approach or strategy used
   - Key technologies or tools utilized
   - Collaboration or leadership aspects
   - Problem-solving or innovation elements

3. Impact (What was the result):
   - Quantifiable metrics and outcomes
   - Business or technical impact
   - Long-term benefits or improvements
   - Recognition or awards received

BULLET POINT EXAMPLES:
Strong bullet points should look like:
- "Led development of [specific project] using [technologies] that [specific impact]"
- "Implemented [specific solution] through [method] resulting in [quantifiable impact]"
- "Designed and executed [specific initiative] by [method] leading to [measurable outcome]"

AVOID:
- Generic statements without specific details
- Vague achievements without metrics
- Overly technical language without context
- Bullet points that don't tell a complete story

OPTIMIZATION STRATEGY:
1. Experience Alignment:
   - Emphasize relevant experiences and achievements
   - Use industry-specific language and terminology
   - Highlight transferable skills and projects
   - Maintain chronological consistency

2. Impact Demonstration:
   - Focus on quantifiable achievements
   - Show progression and growth
   - Demonstrate problem-solving abilities
   - Highlight leadership and initiative

3. Format Preservation:
   - Maintain the original resume format
   - Keep consistent styling and structure
   - Preserve section organization
   - Ensure readability and professionalism

Inputs
Current Resume:
{resume_content}

Job Description:
{job_description}

TASK:
Create an optimized resume that:
1. Maintains the original format and structure
2. Emphasizes relevant experience and achievements
3. Uses industry-specific language
4. Demonstrates clear impact and results
5. Includes detailed, comprehensive bullet points
6. Shows progression and growth
7. Highlights leadership and initiative
8. Maintains authenticity and truthfulness

The resume should:
- Keep the original formatting
- Use clear, specific language
- Include detailed bullet points with action, method, and impact
- Focus on relevant achievements
- Demonstrate quantifiable impact
- Show progression and growth
- Maintain chronological consistency
- Be free of generic statements
- Include industry-specific terminology
- Tell a complete story for each achievement"""

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert resume strategist and hiring consultant with deep experience in optimizing resumes for maximum impact."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
    
    async def generate_cover_letter(self, resume_content: str, job_description: str) -> str:
        prompt = f"""You are an expert cover letter writer and hiring strategist with a talent for crafting compelling narratives that resonate with both the head and heart of the reader. Your task is to create a cover letter that not only demonstrates perfect alignment with the role but also tells a story that makes the reader excited to meet this candidate.

ANALYSIS PHASE:
1. Extract Key Requirements:
   - Identify the 4 most critical requirements from the job description
   - For each requirement, identify specific evidence from the resume
   - Note any innovative ideas or unique value-adds the candidate could bring
   - Consider how these align with company goals and challenges

2. Evaluate as a Time-Pressed Recruiter:
   - What are the key points that must be immediately clear?
   - How can we demonstrate fit in the first paragraph?
   - What metrics or achievements will stand out in a quick scan?
   - How can we make the value proposition obvious?

3. Evaluate as a Detail-Oriented Hiring Manager:
   - What demonstrates strategic thinking?
   - How does the experience translate to this specific role?
   - What innovative ideas or improvements could the candidate bring?
   - How does the candidate's approach align with company culture?

WRITING APPROACH:
1. Opening Hook:
   - Start with a compelling insight about the company or industry
   - Connect it to the candidate's experience and passion
   - Create immediate engagement and curiosity
   - Make the value proposition clear in the first paragraph

2. Key Requirements Alignment:
   - Create a bullet-point section highlighting alignment with the 4 key requirements
   - For each requirement:
     * Show specific evidence from past experience
     * Include relevant metrics or achievements
     * Add innovative ideas or improvements the candidate could bring
     * Connect to company goals or challenges

3. Cultural Fit and Company Knowledge:
   - Analyze the job description for cultural indicators
   - Identify company values and mission
   - Connect the candidate's experience to these cultural elements
   - Show how the candidate's approach aligns with company culture

4. Innovative Value-Add:
   - Identify 2-3 specific ways the candidate could add value
   - Connect these to company goals or challenges
   - Show how past experience supports these ideas
   - Demonstrate strategic thinking and innovation

VOICE AND TONE:
- Enthusiastic but professional
- Executive-level but conversational
- Confident but humble
- Natural and authentic
- Avoid corporate jargon and clichés

STRUCTURE:
1. Engaging Opening:
   - Hook the reader with a relevant insight
   - Show understanding of company context
   - Connect to candidate's passion
   - Make value proposition clear immediately

2. Key Requirements Alignment:
   - Bullet points for each of the 4 key requirements
   - Specific evidence and achievements
   - Innovative ideas and improvements
   - Clear connection to role needs

3. Cultural Connection:
   - Demonstrate understanding of company values
   - Show how candidate's approach fits
   - Share relevant examples of cultural alignment

4. Innovative Value-Add:
   - Specific ideas for improvement
   - Connection to company goals
   - Evidence of past success
   - Strategic thinking

5. Strong Closing:
   - Express genuine excitement about the role
   - Include a specific call to action
   - End with confidence and warmth

Inputs
Candidate Resume:
{resume_content}

Job Description:
{job_description}

TASK:
Write a compelling cover letter that:
1. Opens with an engaging hook that shows understanding of the company
2. Includes a bullet-point section highlighting alignment with the 4 key requirements
3. Demonstrates cultural fit and company knowledge
4. Presents innovative ideas for adding value
5. Uses a professional but conversational tone
6. Tells a story that makes the reader excited to meet the candidate
7. Ends with a confident and warm call to action

The letter should be:
- One page in length
- Addressed to the hiring team
- Include candidate name and contact info at the top
- Written in a natural, engaging style that would sound authentic if read aloud
- Free of corporate clichés and generic statements
- Focused on specific achievements and their impact
- Demonstrating genuine interest in the company and role
- Easy to scan and understand quickly
- Include specific, innovative ideas for adding value"""

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert cover letter writer and hiring strategist with a talent for crafting compelling narratives that resonate with both the head and heart of the reader."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content 