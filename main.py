from flask import Flask, render_template, request
import os
import time
import paramiko

# Paramiko client
try:
    host = "us2.pitunnel.net"
    username = "comfy"
    password = "comfy"
    port = 22156
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password, port = port)
except:
    print('paramiko failed')



# Start flask app
app = Flask(__name__)

# Start tmux
try:
    os.system('tmux kill-session -t bento1')
    os.system('tmux new -s bento1 -d')
    ssh_sequence = 'tmux send-keys "sshpass -p \'comfy\' autossh comfy@us2.pitunnel.net -p 22156" C-m'
    os.system(f"tmux send-keys -t bento1 \'{ssh_sequence}\' Enter")
    os.system("tmux send-keys -t bento1 'hi' Enter")
except:
    print('tmux & autossh failed')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/greet', methods=['POST'])
def greet():
    command = request.form['command']
    os.system(command)
    return 'Hi'

@app.route('/run')
def run():
    os.system("tmux send-keys -t bento1 'python3 dc.py 2 1' Enter")
    #send_command('comfy i2c-dc 1 1 & comfy i2c-dc 2 1')
    return 'hi'

@app.route('/stop')
def stop():
    client.exec_command("comfy i2c-dc 1 0 & comfy i2c-dc 2 0")
    return 'hi'

@app.route('/left')
def left():
    client.exec_command('comfy i2c-dc 1 1 & comfy i2c-dc 2 0')
    return 'hi'

@app.route('/right')
def right():
    client.exec_command('comfy i2c-dc 1 0 & comfy i2c-dc 2 1')
    return 'hi'


@app.route('/test', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        if 'button1' in request.form:
            client.exec_command('comfy i2c-dc 1 1')
            #os.system("tmux send-keys -t bento1 'python3 dc.py 1 1' Enter")
            #send_command('comfy i2c-dc 1 1 & comfy i2c-dc 2 1')
        elif 'button2' in request.form:
            #client.exec_command('comfy i2c-dc 2 1')
            os.system("tmux send-keys -t bento1 'python3 dc.py 2 1' Enter")
            #send_command('comfy i2c-dc 1 0 & comfy i2c-dc 2 0')
        elif 'button3' in request.form:
            client.exec_command('comfy i2c-dc 1 0 & comfy i2c-dc 2 0')
            #os.system("tmux send-keys -t bento1 'python3 dc.py 2 0 & python3 dc.py 1 0' Enter")
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


def send_command(command):
    start_time = time.time()
    
    os.system('tmux send-keys -t bento1 \'' + command + '\' Enter')
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"Command '{command}' took {execution_time:.4f} seconds to execute")
    return 'done'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3389, debug=True)

