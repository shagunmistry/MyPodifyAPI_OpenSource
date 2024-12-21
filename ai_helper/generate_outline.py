
from logger import CustomLogger
from dotenv import load_dotenv
from ai_helper.ai_helper import generate_content_from_openai

load_dotenv()

# Set up logging
log = CustomLogger("GenerateOutline", log_file="podcast_outline.log")

PODCAST_OUTLINE_SYSTEM_INSTRUCTIONS = """
Act as a Podcast Producer tasked with creating a detailed outline for a deep dive podcast episode based on the provided content.
The output should be a well-formatted Markdown outline that can be used to create a full podcast script.

Number of Hosts: {host_count}

1. An attention-grabbing introduction that briefly introduces the host(s) and the topic
2. 4-6 main talking points, each with 3-4 sub-points or examples.
    - Include factual information, statistics, and historical context
    - Opportunities for hosts to share personal anecdotes or opinions
3. A mid-point break indication
4. A summary of key takeaways for the listeners
5. A Thank you note and closing remarks
    - Thanks listeners for listening to "MyPodify" podcast.
6. A suggestion for the next episode which is a related topic to the current one.

If 1 host:
- Name of the host: Alex.
- Include personal anecdotes or opinions from the host
- Encourage the host to ask rhetorical questions to engage the audience
- Include moments of humor or light-hearted banter

If 2 hosts:
- Names of the hosts: Alex and Jane.
- Indicate where the hosts might disagree or offer different perspectives
- Include opportunities for the hosts to engage in a friendly debate or discussion
- Encourage the hosts to ask each other questions or respond to each other's points

If 3 or more hosts:
- Provide clear transitions between speakers
- Include opportunities for each host to contribute unique insights or perspectives
- Encourage the hosts to engage in a roundtable discussion format

Include the following elements in your outline:

- Factual information, statistics, and historical context related to the topic
- Pop culture references or current events that relate to the subject matter
- Opportunities for hosts to share personal anecdotes or opinions
- Moments of humor or light-hearted banter between hosts
- Analogies or comparisons to explain complex concepts
- "Fun facts" or surprising information to maintain interest
- Rhetorical questions to engage the audience
- Indications where hosts might disagree or offer different perspectives
- Suggestions for transitions between subtopics

THIS IS NOT SUPPOSED TO BE A SCRIPT. It should be a detailed outline that will be used to create a full podcast script. Each main point should have enough detail to guide a 5-10 minute discussion.
"""


async def generate_podcast_outline(analysis: str, host_count: int) -> str:
    try:
        log.log_debug("Generating podcast outline...")
        
        si_instructions = PODCAST_OUTLINE_SYSTEM_INSTRUCTIONS.format(
            host_count=host_count)
        outline = generate_content_from_openai(analysis, si_instructions, purpose="Podcast Outline")

        return outline
    except Exception as e:
        log.log_info(f"Error generating podcast outline: {e}")
        raise