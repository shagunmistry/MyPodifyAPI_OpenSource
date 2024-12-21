
from typing import Annotated


from logger import CustomLogger
import aiohttp
from bs4 import BeautifulSoup
import asyncio
from cachetools import TTLCache
import aiodns
import time

logger = CustomLogger(name="MyPodify_Helpers", log_file="mypodify_helpers.log")

# Cache for storing fetched content (1000 items, 1 hour TTL)
content_cache = TTLCache(maxsize=1000, ttl=3600)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'pdf'}

# Rate limiting parameters
rate_limit = 10  # requests per second
last_request_time = time.time()
request_count = 0

async def get_website_content(website_link: str, timeout: int = 10) -> str | None:
    global last_request_time, request_count

    # Check cache first
    if website_link in content_cache:
        return content_cache[website_link]

    # Implement rate limiting
    current_time = time.time()
    if current_time - last_request_time >= 1:
        last_request_time = current_time
        request_count = 0
    if request_count >= rate_limit:
        await asyncio.sleep(1)
        return await get_website_content(website_link, timeout)
    request_count += 1

    try:
        resolver = aiodns.DNSResolver()
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(website_link, timeout=timeout, allow_redirects=True) as response:
                if response.status == 200:
                    html_content = await response.text()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    # Get text content
                    text = soup.get_text()
                    
                    # Clean up text
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = '\n'.join(chunk for chunk in chunks if chunk)
                    
                    # Cache the result
                    content_cache[website_link] = text
                    
                    return text
                else:
                    return f"Failed to fetch content. Status code: {response.status}"
    except asyncio.TimeoutError:
        logger.log_error(f"Timeout fetching website content: {website_link}")
        return None
    except aiohttp.ClientError as e:
        logger.log_error(f"Error fetching website content: {str(e)}")
        return None
    except Exception as e:
        logger.log_error(f"Unknown error fetching website content: {str(e)}")
        return None