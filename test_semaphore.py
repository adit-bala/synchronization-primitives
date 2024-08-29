import synchronization_primitives
import threading
import time

def semaphore_test():
    sem = synchronization_primitives.Semaphore(2)  # Initial value of 2

    def worker(id):
        print(f"Worker {id} attempting to acquire semaphore.")
        sem.sema_down()
        print(f"Worker {id} acquired semaphore.")
        time.sleep(2)  # Simulate some work
        sem.sema_up()
        print(f"Worker {id} released semaphore.")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

def stress_semaphore_test():
    sem = synchronization_primitives.Semaphore(5)  # Initial value of 5
    num_threads = 50
    num_iterations = 20
    count = 0

    def worker():
        nonlocal count
        for _ in range(num_iterations):
            sem.sema_down()
            count += 1
            sem.sema_up()

    threads = [threading.Thread(target=worker) for _ in range(num_threads)]
    start_time = time.time()

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    end_time = time.time()
    print(f"Semaphore test completed in {end_time - start_time:.2f} seconds.")
    print(f"Count value: {count}")

stress_semaphore_test()