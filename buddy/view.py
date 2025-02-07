import subprocess
import time
import signal
import os

def run_nodejs_server(script_path, port=3000):
    """Runs a Node.js server in a subprocess and blocks until the user interrupts it.

    Args:
        script_path: The path to the Node.js server script (e.g., "server.js").
        port: The port the server should listen on (optional, defaults to 3000).
    """

    try:
        # Construct the command to run the Node.js server.
        command = ["node", script_path, str(port)]  # Include the port as an argument if needed

        # Start the Node.js server in a subprocess.
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print(f"Node.js server started on port {port} (PID: {process.pid})")

        # Block until the user interrupts the script (Ctrl+C).
        while True:
            time.sleep(1)  # Check every second (adjust as needed)

            # Check for any output from the server (optional).
            stdout_data = process.stdout.readline().decode().strip()
            if stdout_data:
                print("Server Output:", stdout_data)

            stderr_data = process.stderr.readline().decode().strip()
            if stderr_data:
                print("Server Error:", stderr_data)

            # Check if the process has terminated unexpectedly.
            if process.poll() is not None:
                return_code = process.returncode
                print(f"Node.js server exited with code {return_code}")
                stdout, stderr = process.communicate()
                print("Server stdout:\n", stdout.decode())
                print("Server stderr:\n", stderr.decode())
                return  # Exit if the server crashes.

    except KeyboardInterrupt:
        print("User interrupted. Stopping Node.js server...")
    finally:
        if process:  # Ensure process exists before trying to kill
            # Cleanly terminate the Node.js server.
            os.kill(process.pid, signal.SIGINT)  # Send SIGINT first

            # Give it a little time to shut down gracefully (adjust as needed).
            time.sleep(2)

            if process.poll() is None:  # Check if it's still running
                process.kill()  # Force kill if it hasn't stopped
                print("Node.js server forcefully terminated.")
            else:
                print("Node.js server stopped.")


# Example usage:
if __name__ == "__main__":
    script_path = "./viewer/server.js"  # Replace with the actual path to your server script.
    port = 8080  # Replace with your desired port
    run_nodejs_server(script_path, port)
    print("Python script finished.") # This will print after the server has been killed.