from pypdf import PdfReader
import requests
from gentopia.tools.basetool import *
from typing import AnyStr

class PDFReaderArgs(BaseModel):
	url: str = Field(..., description="the URL to read the PDF.")
	#query: str = Field(..., description="the query string to analyze PDF.")

class PDFReader(BaseTool):

	"""Tool that adds the capability to read PDFs from URLs."""
	name = "pdf_reader"
	description = "A tool to retrieve PDFs through url and analyze the content."
	
	args_schema: Optional[Type[BaseModel]] = PDFReaderArgs
	
	def _run(self, url: AnyStr) -> str:
		try:
			response = requests.get(url)
			with open("sample.pdf", "wb") as pdf_file:
				pdf_file.write(response.content)
				
			pdf_reader = PdfReader("sample.pdf")
			text = ""
			for page_num in range(len(pdf_reader.pages)):
				page = pdf_reader.pages[page_num]
				text += page.extract_text()
			return text
		except Exception as e:
			return f"Error: {e}\n Probably it is an invalid URL."
			
	async def _arun(self, *args: Any, **kwargs: Any) -> Any:
		raise NotImplementedError

if __name__ == "__main__":
	ans = PDFReader()._run("https://arxiv.org/pdf/2407.02067")
	print(ans)