import os
import subprocess
import glob
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import Dict, List

app = FastAPI()

class Model(BaseModel):
    name: str
    requirements_file: str
    status: str = "Not running"

models: Dict[str, Model] = {}

def create_venv(venv_name):
    subprocess.run(['python', '-m', 'venv', venv_name], check=True)

def install_requirements(venv_name, req_file):
    if os.name == 'nt':  # Windows
        pip_path = os.path.join(venv_name, 'Scripts', 'pip')
    else:  # Unix-based systems
        pip_path = os.path.join(venv_name, 'bin', 'pip')
    
    print(f"Using pip: {pip_path}")
    print(f"Installing from: {req_file}")
    
    try:
        result = subprocess.run([pip_path, 'install', '-r', req_file], capture_output=True, text=True, check=True)
        print(f"Installation output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements for {req_file}:")
        print(f"Exit code: {e.returncode}")
        print(f"Error output:\n{e.stderr}")
        print("Continuing with the next environment...")

def setup_environments():
    current_dir = os.getcwd()
    req_files = glob.glob('requirements*.txt')
    
    print(f"Current directory: {current_dir}")
    print(f"Found requirement files: {req_files}")
    
    
    for req_file in req_files:
        venv_name = f"venv_{os.path.splitext(req_file)[0]}"
        venv_path = os.path.join(current_dir, venv_name)
        
        print(f"Creating virtual environment: {venv_name}")
        create_venv(venv_path)
        
        print(f"Installing requirements from: {req_file}")
        install_requirements(venv_path, req_file)
        
        print(f"Virtual environment {venv_name} created and requirements installed.")


def run_model_in_env(model_name: str):
    model = models[model_name]
    venv_name = f"venv_{os.path.splitext(model.requirements_file)[0]}"
    
    if os.name == 'nt':  # Windows
        python_path = os.path.join(venv_name, 'Scripts', 'python')
    else:  # Unix-based systems
        python_path = os.path.join(venv_name, 'bin', 'python')
    
    model_file = f"{model_name}.py"
    if not os.path.exists(model_file):
        raise HTTPException(status_code=404, detail=f"Model file {model_file} not found")
    
    try:
        subprocess.run([python_path, model_file], check=True)
        model.status = "Completed"
    except subprocess.CalledProcessError:
        model.status = "Failed"
        raise HTTPException(status_code=500, detail=f"Error running model {model_name}")

@app.post("/models/")
async def create_model(model: Model):
    if model.name in models:
        raise HTTPException(status_code=400, detail="Model already exists")
    models[model.name] = model
    return {"message": f"Model {model.name} created"}

@app.get("/models/")
async def get_models():
    return list(models.values())

@app.get("/models/{model_name}")
async def get_model(model_name: str):
    if model_name not in models:
        raise HTTPException(status_code=404, detail="Model not found")
    return models[model_name]

@app.post("/models/{model_name}/run")
async def run_model(model_name: str):
    if model_name not in models:
        raise HTTPException(status_code=404, detail="Model not found")
    run_model_in_env(model_name)
    return {"message": f"Model {model_name} is running"}

@app.get("/models/{model_name}/status")
async def get_model_status(model_name: str):
    if model_name not in models:
        raise HTTPException(status_code=404, detail="Model not found")
    return {"status": models[model_name].status}

if __name__ == "__main__":
    setup_environments()
    uvicorn.run(app, host="0.0.0.0", port=8000)