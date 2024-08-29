import synchronization_primitives
import threading
import time

def reader_writer_test():
    rw_lock = synchronization_primitives.RW()
    
    def reader(id):
        rw_lock.rw_lock_acquire(is_reader=True)
        print(f"Reader {id} acquired read lock.")
        time.sleep(1)  # Simulate reading
        rw_lock.rw_lock_release(is_reader=True)
        print(f"Reader {id} released read lock.")
    
    def writer(id):
        rw_lock.rw_lock_acquire(is_reader=False)
        print(f"Writer {id} acquired write lock.")
        time.sleep(2)  # Simulate writing
        rw_lock.rw_lock_release(is_reader=False)
        print(f"Writer {id} released write lock.")

    readers = [threading.Thread(target=reader, args=(i,)) for i in range(3)]
    writers = [threading.Thread(target=writer, args=(i,)) for i in range(2)]

    for t in readers:
        t.start()
    for t in writers:
        t.start()

    for t in readers:
        t.join()
    for t in writers:
        t.join()

def stress_reader_writer_test():
    rw_lock = synchronization_primitives.RW()
    num_readers = 20
    num_writers = 10
    num_iterations = 100

    def reader():
        for _ in range(num_iterations):
            rw_lock.rw_lock_acquire(is_reader=True)
            # Simulate reading
            time.sleep(0.01)
            rw_lock.rw_lock_release(is_reader=True)

    def writer():
        for _ in range(num_iterations):
            rw_lock.rw_lock_acquire(is_reader=False)
            # Simulate writing
            time.sleep(0.02)
            rw_lock.rw_lock_release(is_reader=False)

    reader_threads = [threading.Thread(target=reader) for _ in range(num_readers)]
    writer_threads = [threading.Thread(target=writer) for _ in range(num_writers)]

    start_time = time.time()

    for t in reader_threads:
        t.start()
    for t in writer_threads:
        t.start()
    for t in reader_threads:
        t.join()
    for t in writer_threads:
        t.join()

    end_time = time.time()
    print(f"Reader-Writer test completed in {end_time - start_time:.2f} seconds.")

stress_reader_writer_test()