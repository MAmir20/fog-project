from flask import Flask, render_template, jsonify
import numpy as np
import requests

app = Flask(__name__)

# Matrices to multiply
matrix_A = np.random.randint(1, 10, size=(4, 4))  # Example 4x4 matrix
matrix_B = np.random.randint(1, 10, size=(4, 4))  # Example 4x4 matrix

# Result matrix (initialize with zeros)
result_matrix = np.zeros((4, 4))

# List of fog node addresses (IPs or hostnames)
fog_nodes = ['http://localhost:5001', 'http://localhost:5002']

# Store logs from fog nodes
fog_logs = []

def split_matrix(A, B):
    # Splitting rows between fog nodes
    split_A = np.array_split(A, len(fog_nodes))
    return [(split_A[i], B) for i in range(len(fog_nodes))]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/distribute_tasks', methods=['GET'])
def distribute_tasks():
    global result_matrix, fog_logs
    fog_logs.clear()  # Clear logs for new computation

    # Split the task into sub-tasks
    sub_tasks = split_matrix(matrix_A, matrix_B)

    # Send sub-tasks to each fog node
    for i, node in enumerate(fog_nodes):
        sub_task = {'matrix_A': sub_tasks[i][0].tolist(), 'matrix_B': sub_tasks[i][1].tolist()}
        try:
            response = requests.post(f'{node}/compute', json=sub_task)
            if response.status_code == 200:
                response_data = response.json()

                partial_result = response_data.get('partial_result', None)
                log = response_data.get('log', f"No log received from Fog Node {i + 1}")

                if partial_result:
                    # Append log to the fog_logs list
                    fog_logs.append(f"Fog Node {i + 1}: {log}")

                    # Update result matrix
                    result_matrix[i * len(partial_result):(i + 1) * len(partial_result), :] = partial_result
                else:
                    fog_logs.append(f"Fog Node {i + 1} did not return a partial result.")
            else:
                fog_logs.append(f"Failed to communicate with Fog Node {i + 1}: {response.status_code}")
        except requests.RequestException as e:
            fog_logs.append(f"Failed to send task to {node}: {e}")

    return jsonify(result_matrix.tolist()), 200


@app.route('/get_matrices', methods=['GET'])
def get_matrices():
    return jsonify({
        "matrix_A": matrix_A.tolist(),
        "matrix_B": matrix_B.tolist()
    })

@app.route('/get_logs', methods=['GET'])
def get_logs():
    return jsonify(fog_logs)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
