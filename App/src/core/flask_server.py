# src/core/flask_server.py
import subprocess
import os
import signal
import psutil
from threading import Thread
import time


class FlaskServerManager:
    def __init__(self):
        self.process = None
        self.is_running = False
        self.port = 5000
        self.host = "localhost"
        self.start_time = None
        
    def start_server(self, host="localhost", port=5000, app_path=None):
        """Start the Flask server"""
        if self.is_running:
            return False, "Server is already running"
        
        self.host = host
        self.port = port
        
        try:
            # If app_path is provided, use it; otherwise use default
            if app_path is None:
                app_path = os.path.join(os.getcwd(), "flask_app.py")
            
            # Check if the Flask app file exists
            if not os.path.exists(app_path):
                return False, f"Flask app not found at {app_path}"
            
            # Get the directory and filename
            app_dir = os.path.dirname(app_path) or os.getcwd()
            app_file = os.path.basename(app_path)
            
            # Start Flask using python directly
            cmd = [
                "python",
                app_file,
            ]
            
            # Start the process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Combine stderr with stdout
                stdin=subprocess.PIPE,
                cwd=app_dir,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Give it a moment to start
            import time
            time.sleep(0.5)
            
            # Check if process started successfully
            if self.process.poll() is not None:
                # Process already terminated
                return False, "Server failed to start - check if Flask is installed"
            
            self.is_running = True
            self.start_time = time.time()
            
            return True, f"Server started on {host}:{port}"
            
        except Exception as e:
            return False, f"Failed to start server: {str(e)}"
    
    def stop_server(self):
        """Stop the Flask server gracefully"""
        if not self.is_running or self.process is None:
            return False, "Server is not running"
        
        try:
            # Terminate the process
            self.process.terminate()
            self.process.wait(timeout=5)
            
            self.is_running = False
            self.process = None
            self.start_time = None
            
            return True, "Server stopped successfully"
            
        except subprocess.TimeoutExpired:
            # Force kill if terminate doesn't work
            self.process.kill()
            self.is_running = False
            self.process = None
            self.start_time = None
            return True, "Server force stopped"
            
        except Exception as e:
            return False, f"Failed to stop server: {str(e)}"
    
    def kill_server(self):
        """Force kill the Flask server"""
        if not self.is_running or self.process is None:
            return False, "Server is not running"
        
        try:
            # Force kill
            self.process.kill()
            self.is_running = False
            self.process = None
            self.start_time = None
            
            return True, "Server killed"
            
        except Exception as e:
            return False, f"Failed to kill server: {str(e)}"
    
    def restart_server(self, host=None, port=None, app_path=None):
        """Restart the Flask server"""
        if self.is_running:
            success, msg = self.stop_server()
            if not success:
                return False, msg
            time.sleep(1)  # Wait a bit before restarting
        
        host = host or self.host
        port = port or self.port
        return self.start_server(host, port, app_path)
    
    def get_status(self):
        """Get server status"""
        if self.is_running and self.process:
            # Check if process is actually running
            if self.process.poll() is not None:
                # Process has terminated
                self.is_running = False
                self.process = None
                return {
                    "running": False,
                    "uptime": 0,
                    "host": self.host,
                    "port": self.port
                }
            
            uptime = int(time.time() - self.start_time) if self.start_time else 0
            return {
                "running": True,
                "uptime": uptime,
                "host": self.host,
                "port": self.port,
                "pid": self.process.pid
            }
        
        return {
            "running": False,
            "uptime": 0,
            "host": self.host,
            "port": self.port
        }
    
    def read_output(self, callback=None):
        """Read server output in real-time (run in separate thread)"""
        if not self.process:
            return
        
        def read_stream():
            for line in iter(self.process.stdout.readline, ''):
                if callback:
                    callback(line.strip())
                if not line:
                    break
        
        thread = Thread(target=read_stream, daemon=True)
        thread.start()

