# from ollama import AsyncClient
# from typing import List
# from logger import CustomLogger
# from dotenv import load_dotenv

# load_dotenv()

# log = CustomLogger("AI_Helper", log_file="ai_helper.log")

# # Ollama configuration
# MODEL_NAME = "llama3.2"
# client = AsyncClient()

# async def generate_content_from_ollama(content: str, system_instructions: str, purpose: str,
#                                      previous_content: str = None, chunk_index: int = None,
#                                      total_chunks: int = None) -> str:
#     """Generate content using Ollama's Python library."""
#     log.log_info(f"Generating {purpose} using Ollama...")

#     try:
#         messages = []

#         # Build the system message with context
#         if previous_content and chunk_index is not None:
#             system_msg = (
#                 f"{system_instructions}\n\n"
#                 f"This is part {chunk_index + 1} of {total_chunks}. "
#                 f"Previous content summary:\n{previous_content[:1000]}...\n\n"
#                 f"Continue the {purpose} based on the following additional content, "
#                 f"maintaining consistency with the previous parts:\n\n{content}"
#             )
#         else:
#             system_msg = f"{system_instructions}\n\nContent to analyze:\n\n{content}"

#         messages = [
#             {"role": "system", "content": system_msg},
#             {"role": "user", "content": f"Generate the {purpose} for this content, making it flow naturally with any previous parts."}
#         ]

#         log.log_info(f"Processing content (first 100 chars): {content[:100]}...")

#         response = await client.chat(
#             model=MODEL_NAME,
#             messages=messages,
#             options={
#                 "temperature": 0.7,
#                 "top_p": 0.9
#             }
#         )

#         generated_content = response.message.content
#         log.log_info(f"Generated content (first 100 chars): {generated_content[:100]}...")
#         return generated_content

#     except Exception as e:
#         log.log_error(f"Error generating completion with Ollama: {e}")
#         raise

# async def generate_content_with_chunking(content: str, system_instructions: str, purpose: str) -> str:
#     """Generate content using Ollama with chunking for large inputs."""
#     log.log_info(f"Generating {purpose} with chunking...")

#     def split_content(text: str, chunk_size: int = 8000) -> List[str]:
#         """Split content into chunks based on character count and sentence boundaries."""
#         chunks = []
#         current_chunk = ""

#         # Split by paragraphs first to maintain better context
#         paragraphs = text.split('\n\n')

#         for paragraph in paragraphs:
#             if len(current_chunk) + len(paragraph) < chunk_size:
#                 current_chunk += (paragraph + '\n\n')
#             else:
#                 if current_chunk:
#                     chunks.append(current_chunk.strip())
#                 current_chunk = paragraph + '\n\n'

#         if current_chunk:
#             chunks.append(current_chunk.strip())

#         return chunks

#     try:
#         # If content is small enough, process it directly
#         if len(content) < 8000:
#             return await generate_content_from_ollama(content, system_instructions, purpose)

#         # Split into chunks if content is large
#         chunks = split_content(content)
#         total_chunks = len(chunks)
#         log.log_info(f"Split content into {total_chunks} chunks")

#         final_content = ""
#         for i, chunk in enumerate(chunks):
#             log.log_info(f"Processing chunk {i+1}/{total_chunks}")

#             # Get summary of previous content for context
#             previous_content = final_content if final_content else None

#             chunk_content = await generate_content_from_ollama(
#                 chunk,
#                 system_instructions,
#                 purpose,
#                 previous_content=previous_content,
#                 chunk_index=i,
#                 total_chunks=total_chunks
#             )

#             if i == 0:
#                 final_content = chunk_content
#             else:
#                 # Ensure smooth transition between chunks
#                 final_content += "\n\n" + chunk_content

#             log.log_info(f"Successfully processed chunk {i+1}")

#         return final_content

#     except Exception as e:
#         log.log_error(f"Error in content generation with chunking: {e}")
#         raise
import tiktoken
from openai import OpenAI
import os
from typing import List
from logger import CustomLogger
from dotenv import load_dotenv

load_dotenv()

log = CustomLogger("AI_Helper", log_file="ai_helper.log")

MAX_TOKENS = 128000  # Maximum tokens allowed by the model
BUFFER = 1000  # Buffer for system and user messages

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

MODEL_TO_USE = "gpt-4o-mini-2024-07-18"


def num_tokens_from_string(string: str, model: str = MODEL_TO_USE) -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(string))


def generate_content_from_openai(content: str, system_instructions: str, purpose: str) -> str:
    log.log_debug(f"Generating {purpose} in chunks...")

    def create_completion(messages: List[dict]) -> str:
        completion = client.chat.completions.create(
            model=MODEL_TO_USE,
            messages=messages,
        )
        return completion.choices[0].message.content

    def split_content(content: str, max_tokens: int) -> List[str]:
        chunks = []
        current_chunk = ""
        for line in content.split('\n'):
            line_tokens = num_tokens_from_string(line)
            if num_tokens_from_string(current_chunk) + line_tokens > max_tokens:
                chunks.append(current_chunk)
                current_chunk = line
            else:
                current_chunk += ('\n' if current_chunk else '') + line
        if current_chunk:
            chunks.append(current_chunk)
        return chunks

    log.log_debug(f"Splitting content into chunks...")
    log.log_debug(f"Content length: {len(content)}")

    system_tokens = num_tokens_from_string(system_instructions)
    user_tokens = num_tokens_from_string(
        f"Based on the content provided, generate {purpose}")
    max_chunk_tokens = MAX_TOKENS - system_tokens - user_tokens - BUFFER

    chunks = split_content(content, max_chunk_tokens)
    log.log_debug(f"Split content into {len(chunks)} chunks")

    messages = [
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": f"Based on the content provided, generate {purpose}"},
    ]

    final_content = ""
    for i, chunk in enumerate(chunks):
        chunk_messages = messages.copy()
        chunk_messages.append({"role": "user", "content": chunk})
        if i > 0:
            chunk_messages.append({"role": "user", "content": f"Continue generating the {
                                  purpose} based on this additional content."})

        chunk_content = create_completion(chunk_messages)
        final_content += chunk_content

    log.log_debug(f"Generated {purpose} successfully, processed {
                  len(chunks)} chunks")
    return final_content
