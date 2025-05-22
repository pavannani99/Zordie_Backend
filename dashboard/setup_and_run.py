import os
import subprocess
import sys
import time
from pathlib import Path

def run_command(command, cwd=None):
    try:
        subprocess.run(command, shell=True, check=True, cwd=cwd)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e}")
        return False

def setup_ds_service():
    print("\n=== Setting up Data Science Service ===")
    ds_path = Path("zordie_ds/ResumeIntelligenceSystem")
    
    # Install requirements
    print("\nInstalling requirements...")
    if not run_command("pip install -r requirements.txt", cwd=ds_path):
        return False
    
    # Download spaCy model
    print("\nDownloading spaCy model...")
    if not run_command("python -m spacy download en_core_web_lg"):
        return False
    
    # Test the service
    print("\nTesting the service with sample files...")
    if not run_command("python analyze_resume.py samples/sample_resume.txt samples/sample_job_description.txt", cwd=ds_path):
        return False
    
    return True

def setup_dashboard():
    print("\n=== Setting up Dashboard ===")
    backend_path = Path("Zordie_Backend")
    
    # Install requirements
    print("\nInstalling requirements...")
    if not run_command("pip install -r requirements.txt", cwd=backend_path):
        return False
    
    return True

def run_services():
    print("\n=== Starting Services ===")
    
    # Start data science service
    print("\nStarting Data Science Service...")
    ds_process = subprocess.Popen(
        "python analyze_resume.py samples/sample_resume.txt samples/sample_job_description.txt",
        shell=True,
        cwd="zordie_ds/ResumeIntelligenceSystem"
    )
    
    # Wait a bit for the DS service to start
    time.sleep(2)
    
    # Start dashboard
    print("\nStarting Dashboard...")
    dashboard_process = subprocess.Popen(
        "python -m uvicorn app.dashboard_app:app --reload",
        shell=True,
        cwd="Zordie_Backend"
    )
    
    return ds_process, dashboard_process

def main():
    print("=== Zordie Resume Analysis System Setup ===")
    
    # Setup services
    if not setup_ds_service():
        print("Failed to setup Data Science Service")
        return
    
    if not setup_dashboard():
        print("Failed to setup Dashboard")
        return
    
    # Run services
    ds_process, dashboard_process = run_services()
    
    print("\n=== Services are running! ===")
    print("Dashboard is available at: http://localhost:8000/docs")
    print("Data Science Service is running")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down services...")
        ds_process.terminate()
        dashboard_process.terminate()
        print("Services stopped")

if __name__ == "__main__":
    main() 