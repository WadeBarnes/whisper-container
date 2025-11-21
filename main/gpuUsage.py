# gpuUsage.py

import subprocess

# Function to get GPU usage using nvidia-smi
def get_gpu_usage():
    try:
        result = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE, text=True)
        return result.stdout
    except Exception as e:
        return f"Error retrieving GPU usage: {e}"
