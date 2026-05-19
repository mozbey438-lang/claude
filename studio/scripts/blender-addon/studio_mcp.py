bl_info = {
    "name": "Studio MCP Bridge",
    "author": "Studio",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "description": "Studio backend ile MCP soketi üzerinden iletişim",
    "category": "System",
}

import bpy
import json
import socket
import threading

HOST = "0.0.0.0"
PORT = 6789
_server: socket.socket | None = None
_thread: threading.Thread | None = None


def handle_client(conn: socket.socket):
    with conn:
        for line in conn.makefile("r"):
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
                result = None
                error = None
                if req.get("method") == "execute_python":
                    try:
                        exec_globals = {"bpy": bpy}
                        exec(req["params"]["code"], exec_globals)
                        result = exec_globals.get("_result")
                    except Exception as e:
                        error = str(e)
                elif req.get("method") == "ping":
                    result = "pong"

                resp = {"jsonrpc": "2.0", "id": req.get("id")}
                if error:
                    resp["error"] = {"code": -32000, "message": error}
                else:
                    resp["result"] = result

                conn.sendall((json.dumps(resp) + "\n").encode())
            except Exception as e:
                print(f"[StudioMCP] Hata: {e}")


def server_loop():
    global _server
    _server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    _server.bind((HOST, PORT))
    _server.listen(5)
    print(f"[StudioMCP] Dinleniyor: {HOST}:{PORT}")
    while True:
        try:
            conn, _ = _server.accept()
            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()
        except OSError:
            break


def register():
    global _thread
    _thread = threading.Thread(target=server_loop, daemon=True)
    _thread.start()


def unregister():
    global _server
    if _server:
        _server.close()
