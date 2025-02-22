from flask import Flask
import subprocess
import os

app = Flask(__name__)

@app.route('/run_scraper', methods=['GET'])
def run_scraper():
    try:
        script_path = os.path.join(os.getcwd(), "google_search_automation.py")
        subprocess.Popen(["python", script_path], shell=True)
        return "✅ Script started successfully!", 200
    except Exception as e:
        return f"❌ Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
