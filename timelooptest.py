import schedule
import time
def job():
    print("Hello, World!")

def job_with_argument(name):
    print(f"I am {name}")

schedule.every(5).seconds.do(job)
schedule.every(10).seconds.do(job_with_argument, name="farid")

while True:
    schedule.run_pending()
    # time.sleep(1)