from flask import Flask, request, jsonify
import os
import subprocess
import threading

app = Flask(__name__)

def on_training_success():
    """Called when training completes successfully"""
    print("Training completed successfully!")
    # Add any success handling logic here

def on_training_error(error_code):
    """Called when training fails with an error"""
    print(f"Training failed with error code: {error_code}")
    # Add any error handling logic here

@app.route('/train', methods=['POST'])
def train():
    try:
        # Get prompt from request
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'prompt is required'}), 400
        
        prompt = data['prompt']
        
        # Start subprocess for training
        cmd = ['python', 'main.py', '--config-name=base', f'prompt.prompt={prompt}']
        process = subprocess.Popen(cmd, cwd=os.getcwd())
        
        # Monitor subprocess completion in a separate thread
        def monitor_process():
            return_code = process.wait()
            if return_code == 0:
                on_training_success()
            else:
                on_training_error(return_code)
        
        monitor_thread = threading.Thread(target=monitor_process)
        monitor_thread.start()
        
        return jsonify({'status': 'success', 'message': 'Training started'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

