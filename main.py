from flask import Flask, render_template, request, jsonify
import os
import time
import paramiko
from flask_cors import CORS

# Paramiko client
'''try:
    host = "us2.pitunnel.net"
    username = "comfy"
    password = "comfy"
    port = 22156
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password, port = port)
except:
    print('paramiko failed')'''



# Start flask app
app = Flask(__name__)
CORS(app)
# Start tmux
try:
    os.system('tmux kill-session -t bento1')
    os.system('tmux new -s bento1 -d')
    #ssh_sequence = 'tmux send-keys "sshpass -p \'comfy\' autossh comfy@us2.pitunnel.net -p 22156" C-m'
    ssh_sequence = 'tmux send-keys "sshpass -p \'thomas\' autossh thomas@localhost -p 1111" C-m'
    os.system(f"tmux send-keys -t bento1 \'{ssh_sequence}\' Enter")
    os.system("tmux send-keys -t bento1 'hi' Enter")
except:
    print('tmux & autossh failed')


@app.route('/greet', methods=['POST'])
def greet():
    command = request.form['command']
    os.system(command)
    return 'Hi'

@app.route('/run')
def run():
    os.system("tmux send-keys -t bento1 'python3 dc.py 2 0.7 & python3 dc.py 1 0.7' Enter")
    #send_command('comfy i2c-dc 1 1 & comfy i2c-dc 2 1')
    return 'hi'

@app.route('/stop')
def stop():
    os.system("tmux send-keys -t bento1 'python3 dc.py 2 -0.7 & python3 dc.py 1 -0.7' Enter")
    #client.exec_command("comfy i2c-dc 1 0 & comfy i2c-dc 2 0")
    return 'hi'

@app.route('/left')
def left():
    #client.exec_command('comfy i2c-dc 1 1 & comfy i2c-dc 2 0')
    return 'hi'

@app.route('/right')
def right():
    #client.exec_command('comfy i2c-dc 1 0 & comfy i2c-dc 2 1')
    return 'hi'


@app.route('/old', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'button1' in request.form:
            #client.exec_command('comfy i2c-dc 1 1')
            os.system("tmux send-keys -t bento1 'python3 dc.py 1 1' Enter")
            #send_command('comfy i2c-dc 1 1 & comfy i2c-dc 2 1')
        elif 'button2' in request.form:
            #client.exec_command('comfy i2c-dc 2 1')
            os.system("tmux send-keys -t bento1 'python3 dc.py 2 1' Enter")
            #send_command('comfy i2c-dc 1 0 & comfy i2c-dc 2 0')
        elif 'button3' in request.form:
            #client.exec_command('comfy i2c-dc 1 0 & comfy i2c-dc 2 0')
            os.system("tmux send-keys -t bento1 'python3 dc.py 2 0 & python3 dc.py 1 0' Enter")
            #send_command('comfy i2c-dc 1 0 & comfy i2c-dc 2 0')
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flask Button Example</title>
    </head>
    <body>
        <h1>Flask Button Example</h1>
        <form method="POST">
            <!--<button type="submit" name="button1" style="font-size: 24px; padding: 12px 24px;">run 1</button>-->
            <button type="submit" name="button2" style="font-size: 24px; padding: 12px 24px;">run</button>
            <button type="submit" name="button3" style="font-size: 24px; padding: 12px 24px;">stop</button>
        </form>
        <p>hi</p>
    </body>
    </html>
    """
    return html

@app.route('/', methods=['GET', 'POST'])
def control():
    if request.method == 'POST':
        if 'up' in request.form:
            print('up')
            os.system("tmux send-keys -t bento1 'python3 dc.py 1 1 & python3 dc.py 2 1' Enter")
        elif 'down' in request.form: 
            os.system("tmux send-keys -t bento1 'python3 dc.py 2 -1 & python3 dc.py 1 -1' Enter")
        elif 'left' in request.form:
            os.system("tmux send-keys -t bento1 'python3 dc.py 2 1 & python3 dc.py 1 -1' Enter")
        elif 'right' in request.form:
            os.system("tmux send-keys -t bento1 'python3 dc.py 2 0 & python3 dc.py 1 0' Enter")
    return render_template('controller.html')

@app.route('/bet', methods=['GET', 'POST'])
def ctrl():
    if request.method == 'POST':
        if 'up' in request.form:
            print('up')
            os.system("tmux send-keys -t bento1 'python3 dc.py 1 1 & python3 dc.py 2 1' Enter")
        elif 'down' in request.form: 
            os.system("tmux send-keys -t bento1 'python3 dc.py 2 -1 & python3 dc.py 1 -1' Enter")
        elif 'left' in request.form:
            os.system("tmux send-keys -t bento1 'python3 dc.py 2 1 & python3 dc.py 1 -1' Enter")
        elif 'right' in request.form:
            os.system("tmux send-keys -t bento1 'python3 dc.py 2 0 & python3 dc.py 1 0' Enter")
        
    return render_template('ctrl_test.html')

@app.route('/test')
def test():
    return render_template('grid.html')

def send_command(command):
    start_time = time.time()
    
    os.system('tmux send-keys -t bento1 \'' + command + '\' Enter')
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"Command '{command}' took {execution_time:.4f} seconds to execute")
    return 'done'

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug = True)

