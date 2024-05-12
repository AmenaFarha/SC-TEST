import numpy as np
import threading
import time

def serial_multiplication(m1, m2, row, col):
    result = np.zeros((row, col), dtype=np.int64)
    for i in range(row)
        for j in range(col):
            fo k in range(col):
                result[i, j] += m1[i, k] * m2[k, j]
    return result

def parallel_multiplication_chunk(m1_chunk, m2, result_chunk, thread_id):
    row_chunk, col = m1_chunk.shape
    for i in range(row_chunk):
        for j in range(col):
            s = 0 
            for k in range(col):
                s += m1_chunk[i, k] * m2[k, j]
            result_chunk[i, j] = s

def parallel_matrix_multiplication(m1, m2, row, col):
    # Determine the number of threads based on workload
    num_threads = 4
    result = np.zeros((row, col), dtype=np.int64)
    rows_per_thread = row // num_threads

    threads = []
    for i in range(num_threads):
        start_row = i * rows_per_thread
        end_row = start_row + rows_per_thread
        m1_chunk = m1[start_row:end_row, :]
        result_chunk = result[start_row:end_row, :]
        thread = threading.Thread(target=parallel_multiplication_chunk, args=(m1_chunk, m2, result_chunk, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return result

def generate_matrix(M, row, col, val):
    for i in range(row):
        for j in range(col):
            M[i, j] = val
            val += 1
    return M

if __name__ == '__main__':
    row = 800
    col = 800
    val = 1
    val2 = row * col
    M1 = np.zeros((row, col), dtype=np.int64)
    M2 = np.zeros((col, row), dtype=np.int64)
    
    M1 = generate_matrix(M1, row, col, 1)
    M2 = generate_matrix(M2, col, row, (row * col) + 1)
    
    serial_start_time = time.time()
    result_matrix = serial_multiplication(M1, M2, row, col)
    serial_end_time = time.time()
    serial_execution_time = serial_end_time - serial_start_time
    print(f"Execution time for Serial Matrix Multiplication: {serial_execution_time} seconds")

    parallel_start_time = time.time()
    result_matrix_parallel = parallel_matrix_multiplication(M1, M2, row, col)
    parallel_end_time = time.time()
    parallel_execution_time = parallel_end_time - parallel_start_time
    print(f"Execution time for Parallel Matrix Multiplication: {parallel_execution_time} seconds")
    