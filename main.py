from utils import check_connectivity
import time
from logger import write_log

if __name__ == '__main__':

    while True:

        if check_connectivity():
            write_log("User is connected to the internet.")

        time.sleep(3600) # Checks connection every 1 HR

