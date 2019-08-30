import socketserver
import MySQLdb
import struct



class Server(socketserver.BaseRequestHandler):
    def __init__(self,request,client_address,server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.database = MySQLdb.connect("localhost","root","962424lgj","test",charset='utf8')
        print("[" + self.client_address[0]+"]"+"End server.")

        try:
            self.handle()
        finally:
            print("["+self.client_address[0]+"]"+"End service.")


    def handle(self):
        while True:
            rec = str(self.request.recv(1024),encoding="utf8").split('|')
            
            mydata= rec[0]
            print(mydata)
            if mydata[0] == "3" and mydata[1] == "4":
                if mydata[2] == '3' and mydata[3] == "4":
                    print("in ok")
                    db = MySQLdb.connect("localhost","root","962424lgj","test",charset='utf8')
                    cursor = db.cursor()
                    sql = "INSERT INTO test (item,status,pub_date) VALUES(23,23,NOW());"
                    try:
                        print("execute ok")
                        cursor.execute(sql)
                        db.commit()
                    except:
                        db.rollback()
                    db.close()
                    print("close ok")

if __name__=='__main__':
    socketserver.ThreadingTCPServer(("10.9.7.105",1221),Server).serve_forever()
