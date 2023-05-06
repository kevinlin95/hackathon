import os
import dotenv

dotenv.load_dotenv()


class Config:
    if os.getenv("OPENAI_API_KEY") is None:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
