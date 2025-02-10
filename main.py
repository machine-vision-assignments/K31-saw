import time
import logging

from settings import LOG_FILE
from settings import PRODUCTION
from src.app import App


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logging.info("Application is starting")


app = App()

logging.info("Application started.")


while True:
    t0 = time.time()
    app.update()
    print(f"Running time: {time.time() - t0}")
    if not PRODUCTION:
        time.sleep(0.001)


