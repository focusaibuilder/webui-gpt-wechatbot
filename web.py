from flask import Flask, request, render_template
import json
import subprocess

app = Flask(__name__)

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

@app.route('/', methods=['GET', 'POST'])
def config_and_run():
    with open('config.json', 'r') as f:
        config = json.load(f)
    if request.method == 'POST':
        # 更新配置文件
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
        with open('config.json', 'w') as f:
            json.dump(config, f)
        # 如果点击了"Run App"按钮，那么启动应用程序
        if 'run_app' in request.form:
            subprocess.Popen(['python3', 'app.py'])
    return render_template('index.html', config=config)

if __name__ == '__main__':
    app.run(debug=True)