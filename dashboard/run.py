import uvicorn
import logging
import sys
import socket

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

if __name__ == "__main__":
    try:
        port = 8080
        if is_port_in_use(port):
            logger.error(f"Port {port} is already in use. Please try a different port.")
            sys.exit(1)
            
        logger.info(f"Starting server on port {port}...")
        uvicorn.run(
            "app:app",
            host="localhost",
            port=port,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        sys.exit(1) 