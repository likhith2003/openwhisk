def count_cold_starts(r, W_t, E_t_i, cycle):

    Q_i = [0] * len(r)
    T_i = [0] * len(r)
    L_F_i = E_t_i + W_t

    LF_i = [L_F_i] * len(r)

    Count = 0

    for t in range(cycle):
        for c in range(len(Q_i)):
            if Q_i[c] == 1:  # c is executing
                Q_i[c] = 1
            elif Q_i[c] == 0:  # c is idle
                if t == T_i[c] + E_t_i:
                    Q_i[c] = 0
            elif Q_i[c] == -1:  # c is released
                if t == T_i[c] + LF_i[c]:
                    Q_i[c] = -1

        # Process incoming requests
        for j, r_i in enumerate(r):
            if Q_i[j] == 0 and T_i[j] == min(T_i):
                Q_i[j] = 1
                T_i[j] = t

                if 0 not in Q_i:
                    Count += 1

    return Count

incoming_requests = [1, 1, 1, 0, 0, 1, 0, 1]
warm_time = 3
execution_time = 3
algorithm_cycle = 10

result = count_cold_starts(incoming_requests, warm_time, execution_time, algorithm_cycle)
print("Number of cold starts:", result)
