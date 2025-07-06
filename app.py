from flask import Flask, request, jsonify
import os
import subprocess
import threading
from supabase import create_client, Client

app = Flask(__name__)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def on_training_success(name: str, path: str):
    """Called when training completes successfully"""
    print(f"Training completed successfully for {name}. Exporting as ply...")

    # Execute the export command
    cmd = ['python', '-m', 'utils.export', name, '--type', 'ply']
    try:
        subprocess.run(cmd, check=True)
        print(f"Exported {name} to {path}")

        # Upload the exported file to Supabase storage
        with open(f"exports/ply/{name}.ply", "rb") as f:
            response = supabase.storage.from_("splats").update(
                file=f,
                path=path
            )
            print(f"File uploaded to Supabase: {response.fullPath}")
    except subprocess.CalledProcessError as e:
        print(f"Export failed: {e}")

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

        # Create the supabase file
        with open('exports/empty.ply', "rb") as f:
            # Name of the splat
            name = prompt.strip().replace(" ", "_").lower()[:64]

            response = supabase.storage.from_("splats").upload(
                file=f,
                path=name
            )
            
            # Monitor subprocess completion in a separate thread
            def monitor_process():
                return_code = process.wait()
                if return_code == 0:
                    on_training_success(name, response.fullPath)
                else:
                    on_training_error(return_code)

            monitor_thread = threading.Thread(target=monitor_process)
            monitor_thread.start()
            
            return jsonify({'status': 'success', 'url': response.fullPath}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

