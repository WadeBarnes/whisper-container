# Whisper Container

*Whisper AI in a GPU‑enabled container.*


## 📦 Prerequisites

| Item | Requirement | Notes |
|------|-------------|-------|
| **CUDA** | Installed on the host machine | The container must be able to access a GPU, ie ensure the container runtime is configured to expose the GPU (e.g., `--gpus all` for Docker). |
| **Container runtime** | Docker, OpenShift, or any OCI‑compatible platform | The runtime must expose the host GPU to the container. |
| **Docker Compose** |  | Used for building and running the stack locally. |

> **⚠️** At the moment this project is built to run with CUDA on Nvidia GPU's.


## 🚀 Usage

```bash
# Build the image
docker compose build

# Start the container in detached mode
docker compose up -d
```

On the first run the container will create the following directories under `data/`:

| Directory | Purpose |
|-----------|---------|
| `input_audio` | Place the audio files you want to transcribe here. |
| `logs` | Default log output. |
| `model_cache` | Cached Whisper models. You can pre‑populate this with downloaded models. |
| `transcripts` | Output folder. Each transcription is stored in a sub‑folder named: `<audio_file>__<model_used>__<timestamp>`. |

> **Tip:** After the container is running, you can add new audio files to `input_audio` for the container to process.


## ⚙️ Configuration

Settings are defined in `main/config.py`. Settings are setup to be as accurate and consistant as possible.


## 🐛 Debugging

1. **Enable the keep‑alive command**\
   In `docker-compose.yaml`, comment out the `entrypoint` line and uncomment the `keep alive` command.

2. **Rebuild & restart**
   ```bash
   docker compose build
   docker compose up -d
   ```

3. **Attach to the running container**
   ```bash
   docker exec -it whisper-container bash
   ```

4. **Run Transcription Manually**
   ```bash
   python3 main.py
   ```

## ⚠️ Known Issues

| Issue | Description | Work‑around |
|-------|-------------|-------------|
| `Failed to launch Triton kernels` | Occurs when CUDA toolkits are not installed in the container. | If needed uncomment `wget`, `Set Up Cuda Repos`, and `Install Cuda Repos` sections in the Dockerfile. This was done to decrease the size of the container image to under 10 GB from ~40 GB. |
