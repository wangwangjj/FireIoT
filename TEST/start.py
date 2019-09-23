from ./BaseServer import BaseServer
import SocketServer
addr = (host,port)
log.debug(addr)
# 解决地址被占用问题，这个很重要，不然重启服务的时候总是提示地址被占用了
SocketServer.TCPServer.allow_reuse_address = True
server = SocketServer.ThreadingTCPServer(addr, BaseServer)
server.serve_forever()

