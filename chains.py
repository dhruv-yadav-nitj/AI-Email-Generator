import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

load_dotenv()


class Chain:
    def __init__(self):
        key = os.getenv('GROQ_API_KEY')
        self.llm = ChatGroq(
            groq_api_key=key,
            model="llama3-8b-8192",
            temperature=1,
            max_tokens=None,
            max_retries=3,
            timeout=None
        )

    def write_mail(self, job, links):
        prompt = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}
            ### INSTRUCTION:
            You are Dhruv Yadav, a Business Development Executive (BDE) at DGDC IT. DGDC IT is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of DGDC IT 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase DGDC IT portfolio: {link_list}
            Remember you are Dhruv Yadav, BDE at DGDC IT. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain = prompt | self.llm
        result = chain.invoke({
            "job_description": str(job),
            "link_list": links
        })
        return result.content

    def extract_jobs(self, text):
        prompt = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the 
            following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain = prompt | self.llm
        result = chain.invoke({
            "page_data": text
        })
        try:
            json = JsonOutputParser()
            result = json.parse(result.content)
            return result if isinstance(result, list) else [result]  # we want to return the list of jobs available
        except Exception as e:
            raise OutputParserException("Retry!")
