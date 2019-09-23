import socketserver
import struct
 
# 自定义类来实现通信循环
class MyTCPHandler(socketserver.BaseRequestHandler):
    # 必须写入handle方法，建立链接时会自动执行handle方法
    def handle(self):
        while True:
            try:
                data = self.request.recv(1024)
                if not data: break
                print('->client:', data.hex())
                print('change:',data)
                head,num,vertion,time,n1,n2,len1,len2,cmd=struct.unpack("!3H6s6s6s3B",data[:27])
                length=len2*256+len1
                head,num,vertion,time,n1,n2,len1,len2,cmd,msg,checksum,end=struct.unpack("!3H6s6s6s3B"+str(length)+"sHB",data)
                print(msg)
                msg.replace(msg[0:1],b'\xFF')
                print(msg)
                self.request.send(data)
            except ConnectionResetError:
                break
        self.request.close()
 
 
if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('10.9.7.105', 1221), MyTCPHandler)
    server.serve_forever()  # 链接循环
