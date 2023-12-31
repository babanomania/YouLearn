
from langchain.text_splitter import TokenTextSplitter
from langchain.document_loaders import YoutubeLoader
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from lib.model import get_llm


def load_video_captions(url):
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
    return loader.load()


def tokeize_as_summary(data):
    # Initialize text splitter for summary (Large chunks for better context and less API calls)
    text_splitter_summary = TokenTextSplitter(
        chunk_size=10000, chunk_overlap=250)
    return text_splitter_summary.split_documents(data)


def tokeize_as_qa(data):
    # Initialize text splitter for QA (Smaller chunks for better QA)
    text_splitter_qa = TokenTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter_qa.split_documents(data)


def generate_summary(docs_summary):

    # Prompts for summary

    # The first prompt is for the initial summarization of a chunk. You can add any info about yourself or the topic you want.
    # You could specifically focus on a skill you have to get more relevant results.
    summary_template = """
        You are an expert in summarizing YouTube videos.
        You're goal is to create a summary of a podcast.
        Below you find the transcript of a podcast:
        ------------
        {text}
        ------------

        The transript of the podcast will also be used as the basis for a question and answer bot.
        Provide some examples questions and answers that could be asked about the podcast. Make these questions very specific.

        Your output should use the following template:
        ### Summary
        ### Analogy
        ### Notes
        - [Emoji] Bulletpoint
        ### Keywords
        - Explanation
        ### Example Questions

        You have been tasked with creating a concise summary of a YouTube video using its transcription to supply college student notes to use himself. You are to act like an expert in the subject the transcription is written about.

        Make a summary of the transcript. Use keywords from the transcript. Don't explain them. Keywords will be explained later.

        Additionally make a short complex analogy to give context and/or analogy from day-to-day life from the transcript.

        Create 10 bullet points (each with an appropriate emoji) that summarize the key points or important moments from the video's transcription.

        In addition to the bullet points, extract the most important keywords and any complex words not known to the average reader aswell as any acronyms mentioned. For each keyword and complex word, provide an explanation and definition based on its occurrence in the transcription.

        You are also a transcription AI and you have been provided with a text that may contain mentions of sponsorships or brand names. Your task write what you have been said to do while avoiding any mention of sponsorships or brand names.

        Please ensure that the summary, bullet points, and explanations fit within the 330-word limit, while still offering a comprehensive and clear understanding of the video's content. 
    """

    PROMPT_SUMMARY = PromptTemplate(
        template=summary_template, input_variables=["text"])

    # The second prompt is for the refinement of the summary, based on subsequent chunks.
    summary_refine_template = (
        """
        You are an expert in summarizing YouTube videos.
        You're goal is to create a summary of a podcast.
        We have provided an existing summary up to a certain point: {existing_answer}
        We have the opportunity to refine the summary
        (only if needed) with some more context below.
        Below you find the transcript of a podcast:
        ------------
        {text}
        ------------
        Given the new context, refine the summary and questions.
        The transript of the podcast will also be used as the basis for a question and answer bot.
        Provide some examples questions and answers that could be asked about the podcast. Make these questions very specific.
        If the context isn't useful, return the original summary and questions.
        
        Your output should use the following template:
        ### Summary
        ### Analogy
        ### Notes
        - [Emoji] Bulletpoint
        ### Keywords
        - Explanation
        ### Example Questions

        You have been tasked with creating a concise summary of a YouTube video using its transcription to supply college student notes to use himself. You are to act like an expert in the subject the transcription is written about.

        Make a summary of the transcript. Use keywords from the transcript. Don't explain them. Keywords will be explained later.

        Additionally make a short complex analogy to give context and/or analogy from day-to-day life from the transcript.

        Create 10 bullet points (each with an appropriate emoji) that summarize the key points or important moments from the video's transcription.

        In addition to the bullet points, extract the most important keywords and any complex words not known to the average reader aswell as any acronyms mentioned. For each keyword and complex word, provide an explanation and definition based on its occurrence in the transcription.

        You are also a transcription AI and you have been provided with a text that may contain mentions of sponsorships or brand names. Your task write what you have been said to do while avoiding any mention of sponsorships or brand names.

        Please ensure that the summary, bullet points, and explanations fit within the 330-word limit, while still offering a comprehensive and clear understanding of the video's content. .
    """
    )

    PROMPT_SUMMARY_REFINE = PromptTemplate(
        input_variables=["existing_answer", "text"],
        template=summary_refine_template,
    )

    # Initialize LLM
    llm_summary = get_llm()

    # Initialize summarization chain
    summarize_chain = load_summarize_chain(
        llm=llm_summary,
        chain_type="refine",
        verbose=True,
        question_prompt=PROMPT_SUMMARY,
        refine_prompt=PROMPT_SUMMARY_REFINE
    )
    summary = summarize_chain.run(docs_summary)

    return summary


def create_qa_chain(docs_qa):

    # Create the LLM model for the question answering
    llm_question_answer = get_llm()

    # Create the vector database and RetrievalQA Chain
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs_qa, embeddings)
    qa = RetrievalQA.from_chain_type(
        llm=llm_question_answer,
        chain_type="stuff",
        retriever=db.as_retriever()
    )

    return qa
