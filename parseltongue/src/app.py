import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for
import tempfile

app = Flask(__name__)

# Path to the script that processes the YAML file
SCRIPT_PATH = "parseltongue_generator.py"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        yaml_file = request.files["yaml_file"]
        if yaml_file:
            # Create a temporary file to store the uploaded YAML
            with tempfile.NamedTemporaryFile(delete=False) as temp_yaml:
                temp_yaml.write(yaml_file.read())
                temp_yaml_path = temp_yaml.name

            # Call the script to process the temporary YAML file
            try:
                result = subprocess.check_output(["python", SCRIPT_PATH, temp_yaml_path], text=True, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                result = e.output

            # Clean up the temporary YAML file
            os.remove(temp_yaml_path)

            return render_template("index.html", result=result)

    return render_template("index.html", result=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
