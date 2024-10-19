from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/compute', methods=['POST'])
def compute():
    data = request.get_json()

    # Extract matrices A and B from the request
    matrix_A = np.array(data['matrix_A'])
    matrix_B = np.array(data['matrix_B'])

    # Perform matrix multiplication
    partial_result = np.dot(matrix_A, matrix_B)

    # Log what this node is calculating (can also be saved to a file for local tracking)
    log = f"Calculating: A (rows {matrix_A.shape[0]}) x B (size {matrix_B.shape})"

    # Return the result and the log
    return jsonify({
        'partial_result': partial_result.tolist(),
        'log': log
    })

if __name__ == "__main__":
    app.run(port=5002, debug=True)  # Change port for each fog node
