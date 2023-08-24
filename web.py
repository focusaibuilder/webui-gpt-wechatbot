from flask import Flask, request, render_template
import json
import subprocess
import sys
import os
import shutil



app = Flask(__name__)

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

@app.route('/', methods=['GET', 'POST'])
def config_and_run():
    config_file = f'config_{instance_id}.json'
    if not os.path.exists(config_file):
        shutil.copy2('config.json', config_file)

    with open(config_file, 'r') as f:
        config = json.load(f)

    if request.method == 'POST':
        for key, value in request.form.items():
            if key != 'run_app':
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                elif value.isdigit():
                    value = int(value)
                elif is_float(value):
                    value = float(value)
                config[key] = value

        with open(config_file, 'w') as f:
            json.dump(config, f)

        if 'run_app' in request.form:
            env = os.environ.copy()
            env["INSTANCE_ID"] = str(instance_id)
            subprocess.Popen(['python3', 'app.py'], env=env)


    return render_template('index.html', config=config)

if __name__ == '__main__':
    instance_id = sys.argv[1] if len(sys.argv) > 1 else "default"
    port = 5000 + int(instance_id)  # 为每个实例选择一个独特的端口

    app.run(debug=True, port=port)
