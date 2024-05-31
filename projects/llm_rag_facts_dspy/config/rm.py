import dspy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_rm():
    # Set up the retrieval model
    return dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')
