import threading
import time

def process_container_state_change(csc, rt, rtrunning, rtpaused):
    if csc == "CREATED":
        rtrunning += 1
    elif csc == "PAUSED":
        rtrunning -= 1
        rtpaused += 1
    elif csc == "REUSED":
        rtpaused -= 1
        rtrunning += 1
    elif csc == "EVICTED":
        rtpaused -= 1

    print(f"Container State Change: {csc}, rtrunning: {rtrunning}, rtpaused: {rtpaused}")

def simulate_periodic_requests():
    # Simulate requests every 15 seconds for 3 minutes
    for _ in range(12):  # 4 requests per minute for 3 minutes
        time.sleep(15)  # Simulate 15 seconds interval
        process_container_state_change("CREATED", "GET", rtrunning_initial, rtpaused_initial)

# Example Usage:
# Initialize variables
rtrunning_initial = 0
rtpaused_initial = 0

# Create a thread to simulate periodic requests
request_thread = threading.Thread(target=simulate_periodic_requests)
request_thread.start()

# Simulate container state changes
process_container_state_change("PAUSED", "POST", rtrunning_initial, rtpaused_initial)
time.sleep(3)  # Simulate the execution time of a request (3 seconds)

process_container_state_change("REUSED", "PUT", rtrunning_initial, rtpaused_initial)
time.sleep(3)

process_container_state_change("EVICTED", "DELETE", rtrunning_initial, rtpaused_initial)
time.sleep(3)

# Wait for the request thread to finish
request_thread.join()





# Simulate container state changes
process_container_state_change("CREATED", "GET", rtrunning_initial, rtpaused_initial)
print(f"rtrunning: {rtrunning_initial}, rtpaused: {rtpaused_initial}")

process_container_state_change("PAUSED", "POST", rtrunning_initial, rtpaused_initial)
print(f"rtrunning: {rtrunning_initial}, rtpaused: {rtpaused_initial}")

process_container_state_change("REUSED", "PUT", rtrunning_initial, rtpaused_initial)
print(f"rtrunning: {rtrunning_initial}, rtpaused: {rtpaused_initial}")

process_container_state_change("EVICTED", "DELETE", rtrunning_initial, rtpaused_initial)
print(f"rtrunning: {rtrunning_initial}, rtpaused: {rtpaused_initial}")
