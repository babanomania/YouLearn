
import chainlit as cl

from lib.core import load_video_captions, tokeize_as_summary, tokeize_as_qa, generate_summary, create_qa_chain

# take environment variables from .env.
from dotenv import load_dotenv
load_dotenv()


@cl.langchain_factory(use_async=True)
async def init():

    res = await cl.AskUserMessage(
        content="Please provide a youtube url to begin!",
    ).send()

    youtube_url = res['content']

    msg = cl.Message(content=f"Processing video...")
    await msg.send()

    # Load a youtube video and get the transcript
    video_captions = load_video_captions(youtube_url)

    # Split text into docs for summary
    captions_summary = tokeize_as_summary(video_captions)

    # Split text into docs for QA
    captions_qa_text = tokeize_as_qa(video_captions)

    summary_txt = generate_summary(captions_summary)

    qa_chain = create_qa_chain(captions_qa_text)
    cl.user_session.set("qa_chain", qa_chain)

    # Let the user know that the system is ready
    await msg.update(content=f"Video processed. Here is what i found")
    await cl.Message(content=summary_txt).send()
    await cl.Message(content=f"You can now ask questions").send()

    return qa_chain
