import subprocess
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

def setup_dashboard():
    print("\n=== Setting up Dashboard ===")
    backend_path = Path("Zordie_Backend")
    
    # Install requirements
    print("\nInstalling requirements...")
    if not run_command("pip install -r requirements.txt", cwd=backend_path):
        return False
    
    return True

def run_dashboard():
    print("\n=== Starting Dashboard ===")
    backend_path = Path("Zordie_Backend")
    
    # Start dashboard
    print("\nStarting Dashboard...")
    dashboard_process = subprocess.Popen(
        "python -m uvicorn app.dashboard_app:app --reload",
        shell=True,
        cwd=backend_path
    )
    
    return dashboard_process

def main():
    print("=== Zordie Dashboard Setup ===")
    
    # Setup dashboard
    if not setup_dashboard():
        print("Failed to setup Dashboard")
        return
    
    # Run dashboard
    dashboard_process = run_dashboard()
    
    print("\n=== Dashboard is running! ===")
    print("Dashboard is available at: http://localhost:8000/docs")
    print("\nYou can test the dashboard with these endpoints:")
    print("1. POST /dashboard/analyze-resume - Upload resume and job description")
    print("2. GET /dashboard/analysis-history - View all analyses")
    print("3. GET /dashboard/analysis/{analysis_id} - View specific analysis")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down dashboard...")
        dashboard_process.terminate()
        print("Dashboard stopped")

if __name__ == "__main__":
    main() 