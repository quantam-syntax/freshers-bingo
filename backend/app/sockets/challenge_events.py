from flask_socketio import emit


def register_socket_handlers(socketio):

    @socketio.on("connect")
    def handle_connect():
        emit("connected", {"status": "ok"})

    @socketio.on("disconnect")
    def handle_disconnect():
        pass
