# YouTube Q&A BOT

from langchain.callbacks import get_openai_callback
from core import load_video_captions, tokeize_as_summary, tokeize_as_qa, generate_summary, create_qa_chain

# take environment variables from .env.
from dotenv import load_dotenv
load_dotenv()

with get_openai_callback() as cb:

    youtube_url = input("please provide a youtube url to start: ")
    # Load a youtube video and get the transcript
    data = load_video_captions(youtube_url)

    # Split text into docs for summary
    docs_summary = tokeize_as_summary(data)

    # Generate summary from youtube captions
    summary = generate_summary(docs_summary)
    print(summary)

    # Split text into docs for QA
    docs_qa = tokeize_as_qa(data)

    # Create the qa chain for the question answering
    qa = create_qa_chain(docs_qa)

    question = ""
    # Run the QA chain continuously
    while question != "exit":
        # Get the user question
        question = input("Ask a question or enter exit to close the app: ")
        # Run the QA chain
        answer = qa.run(question)
        print(answer)
        print("---------------------------------")
        print("\n")

print(cb)
