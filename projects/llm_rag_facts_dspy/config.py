# import os

# from dotenv import load_dotenv

# load_dotenv()


class Config:
    optimize = {

    },
    evaluate = {
        "num_threads": 4,
        "display_progress": True,
        "display_table": 0
    },
    inference = {
    }
    # SESSION_PERMANENT = True
    # SECRET_KEY = os.environ["SECRET_KEY"]
    # CELERY = {
    #     "broker_url": os.environ.get("REDIS_URI", False),
    #     "task_ignore_result": True,
    # }
