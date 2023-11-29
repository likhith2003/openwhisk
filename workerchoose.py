import random
import time
import threading
from queue import Queue

def generate_hash(request):
    return hash(request) % 10, 1

def get_request_type_info(worker, request):
    rtpaused = 0
    rtrunning = 0
    wfree = 100
    wfree_and_cached = 150
    rrequired = 50
    return rtpaused, rtrunning, wfree, wfree_and_cached, rrequired

def process_request(request, worker, request_queue):
    time.sleep(10)  # Simulate the execution time of a request
    print(f"{time.strftime('%H:%M:%S')} - Request processed by {worker}: {request}")
    request_queue.put(worker)

def create_worker(worker_id):
    time.sleep(5)  # Simulate the time to create a new worker
    print(f"{time.strftime('%H:%M:%S')} - New worker created: {worker_id}")

def worker_process(worker_id, request_queue):
    while True:
        request = request_queue.get()
        if request is None:
            break

        process_request(request, worker_id, request_queue)
        request_queue.task_done()

def simulate_periodic_requests(request_queue):
    for _ in range(180):  # 15 requests per minute for 3 minutes
        time.sleep(4)  # Simulate 4 seconds interval
        request_queue.put(f"Request-{random.randint(1, 100)}")

def main():
    workers = ["Worker1", "Worker2", "Worker3", "Worker4"]
    request_queue = Queue()

    # Create worker threads
    worker_threads = []
    for worker_id in workers:
        worker_thread = threading.Thread(target=worker_process, args=(worker_id, request_queue))
        worker_thread.start()
        worker_threads.append(worker_thread)

    # Create a thread to simulate periodic requests
    request_thread = threading.Thread(target=simulate_periodic_requests, args=(request_queue,))
    request_thread.start()

    try:
        while True:
            if not request_queue.empty():
                request = request_queue.get()
                worker = choose_worker(request, workers)
                if worker is None:
                    print(f"{time.strftime('%H:%M:%S')} - No available workers. Creating a new worker.")
                    new_worker_id = f"Worker{len(workers) + 1}"
                    workers.append(new_worker_id)
                    create_worker(new_worker_id)
                    worker = new_worker_id

                request_queue.task_done()

                # Limit each worker to process only 2 requests at a time
                if threading.active_count() < 12:  # Maximum 12 threads (4 workers * 2 requests each)
                    worker_thread = threading.Thread(target=worker_process, args=(worker, request_queue))
                    worker_thread.start()
                    worker_threads.append(worker_thread)
            else:
                time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted. Cleaning up threads.")

    # Add None to the queue for each worker to exit gracefully
    for _ in workers:
        request_queue.put(None)

    # Wait for worker threads to finish
    for worker_thread in worker_threads:
        worker_thread.join()

    # Wait for the request thread to finish
    request_thread.join()

if __name__ == "__main__":
    main()
