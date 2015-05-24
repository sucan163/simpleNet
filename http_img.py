#!/usr/bin/env python
# coding=utf-8

from daemon import Daemon
import socket
import time

html = """HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nContent-Length: """
html404 = """HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: 14\r\n\r\n<h1>404 </h1>"""

class agentD(Daemon):
    def run(self):
        listen_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        listen_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_fd.bind(("0.0.0.0", 9000))
        listen_fd.listen(10)
        while True:
            conn, addr = listen_fd.accept()
            print "coming", conn, addr
            read_data = conn.recv(100)
            print read_data
            pic_name = read_data.split(" ")[1][1:]
            print pic_name
            try:
                with file(pic_name) as f:
                    pic_content = f.read()
                    length = len(pic_content)
                    html_resp = html
                    html_resp += "%d\r\n\r\n" % (length)
                    print html_resp
                    html_resp += pic_content
            except:
                html_resp = html404
            conn.send(html_resp)
            conn.close()

if __name__ == "__main__":
    agentd = agentD(pidfile="agentd.pid", stdout="agentd.log", stderr="agentd.log")
    agentd.run()
