import SocketServer,socket
from control import *
svsocket = getconfig()['svsocket']
class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads = True
    log.debug('server start.')

class BaseServer(SocketServer.BaseRequestHandler):

    ip = ""
    port = 0
    timeOut = svsocket['TIMEOUT']     # 设置超时时间变量

    client_addr = []
    client_socket = []

    def setup(self):
        try:
            self.ip = self.client_address[0].strip()     # 获取客户端的ip
            self.port = self.client_address[1]           # 获取客户端的port
            self.request.settimeout(self.timeOut)        # 对socket设置超时时间
            log.debug('join_client:{}:{}'.format(self.ip,self.port))
            self.client_addr.append(self.client_address) # 保存到队列中
            self.client_socket.append(self.request)      # 保存套接字socket
            log.debug('all_clint:{}'.format(self.client_addr))
        except BaseException as e:
            log.error(e)

    def finish(self):
        """
        这个方法会执行2次，第二次执行的时候必然报错 ，故pass
        :return:
        """
        try:
            self.client_addr.remove(self.client_address)
            self.client_socket.remove(self.request)
            log.debug('disconnect_client:{}:{}'.format(self.ip,self.port))
        except:
            pass

    def handle(self):
        # 主要的处理业务函数
        while True:
            try:
                try:
                    self.recvdata_ori = self.request.recv(2048)
                except socket.timeout:  # 如果接收超时会抛出socket.timeout异常
                    log.warning('port:{}-timeout_client:{}:{}'.format(self.port, self.ip, self.port))
                    break       # 记得跳出while循环
                if self.recvdata_ori:    # 判断是否接收到数据
                    recv = json.loads(self.recvdata_ori)
                    log.debug('recv:{}'.format(recv))
                    if recv.has_key('who'):
                        if 'sts'==recv['who']:
                            resp = insert_sts(recv)
                        elif 'ap_kaoji' == recv['who']:
                            resp = insert_ap(recv)
                        elif 'ap_test' == recv['who']:
                            resp = insert_ap_test(recv)
                else:
                    self.finish()
            except BaseException as e:
                log.error(e)
                raise e

    def send(self,data):
        try:
            result = self.request.send(data)
            log.debug('send_result:{}'.format(result))
        except BaseException as e:
            log.error(e)
