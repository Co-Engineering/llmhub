import asyncio
import base64

from pydantic import BaseModel

from llmhub.core.llms import BaseGenerationModel, LLMClientAsync

with open("/home/svane/projects/birdie/birdie_jobs/test.pdf", "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")


client = LLMClientAsync(["anthropic", "gemini"])
contents = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "please tell me about copenhagen. keep it very brief",
            },
            {
                "type": "input_file",
                "file_data": encoded,
                "file_name": "test.pdf",
            },
        ],
        "type": "message",
    }
]


class ResponseModel(BaseModel):
    info: str
    source: str


generation_model = BaseGenerationModel(
    model="gemini-2.5-flash",
    messages=contents,
    system="You are a helpfull assistant",
    # response_schema=ResponseModel,
    max_tokens=1024,
)
print(asyncio.run(client.create_generation(generation_model, "gemini")))
