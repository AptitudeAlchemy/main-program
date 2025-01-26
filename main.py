from utils import check_connectivity
import time

if __name__ == '__main__':

    while True:

        if check_connectivity():
            print("User is connected to the internet.")

        time.sleep(3600) # Checks connection every 1 HR

