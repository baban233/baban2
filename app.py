from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

HTML = '''
<!DOCTYPE html>
<html>
<head><title>Live Bildschirm Stream</title></head>
<body style="background:#111;color:#eee; text-align:center; margin:0; padding:20px;">
  <h1>Live Bildschirm Stream</h1>
  <img id="stream" style="max-width: 100vw; max-height: 90vh; border: 3px solid #0af; border-radius: 10px;">
  <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
  <script>
    const socket = io();
    const img = document.getElementById('stream');
    socket.on('frame', data => {
      img.src = 'data:image/jpeg;base64,' + data;
    });
  </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@socketio.on('frame')
def handle_frame(data):
    # Broadcast an alle anderen Clients außer Sender
    emit('frame', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
