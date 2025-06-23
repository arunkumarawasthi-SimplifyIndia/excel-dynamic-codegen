import subprocess
import sys
import webbrowser
import time

print("Starting Streamlit...")

# Start Streamlit app and capture logs
proc = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", "app.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Wait a few seconds
time.sleep(5)

# Print early output (debug log)
stdout, stderr = proc.communicate(timeout=10)
print("STDOUT:\n", stdout)
print("STDERR:\n", stderr)

# Try to open browser
try:
    print("Opening browser at http://localhost:8501")
    webbrowser.open("http://localhost:8501")
except Exception as e:
    print("⚠ Could not open browser:", e)

input("Press Enter to exit...")
