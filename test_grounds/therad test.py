import threading
import time

def worker_function(name, delay):
    print(f"Worker {name} started")
    time.sleep(delay)
    print(f"Worker {name} ended after {delay} seconds")

thread1 = threading.Thread(target=worker_function, args=("Alpha", 10))

thread2 = threading.Thread(target=worker_function, args=("Beta", 20))
thread3 = threading.Thread(target=worker_function, args=("Charlie", 30))
thread4 = threading.Thread(target=worker_function, args=("Delta", 40))

thread1.start()
thread2.start()
thread3.start()
thread4.start()

thread1.join()
print("Main Program complete")



