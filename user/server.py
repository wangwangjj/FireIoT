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
                    db = MySQLdb.connect("localhost","root","962424lgj","FireData",charset='utf8')
                    cursor = db.cursor()
                    sql = "INSERT INTO Data (huilu,addr,item,state,pub_date) VALUES("+mydata[8]+","+mydata[9]+",\""+str(self.returnitem(mydata[4],mydata[5]))+"\",\""+str(self.returnstate(mydata[6],mydata[7]))+"\",NOW());"
                    print(sql)
                    try:
                        print("execute ok")
                        cursor.execute(sql)
                        db.commit()
                    except:
                        db.rollback()
                    db.close()
                    print("close ok")
                    
    def returnstate(self,data1,data2):
        if data1 == '8' and data2 == '0':
            return "火警"
        elif data1 == '8' and data2 == '1':
            return "地址故障"
        elif data1 == '8' and data2 == '2':
            return "地址故障恢复"
        elif data1 == '8' and data2 == '3':
            return "自动启动"
        elif data1 == '8' and data2 == '4':
            return "启动撤销"
        elif data1 == '8' and data2 == '5':
            return "反馈"
        elif data1 == '8' and data2 == '6':
            return "反馈撤销"
        elif data1 == '8' and data2 == '7':
            return "回路故障"
        elif data1 == '8' and data2 == '8':
            return "回路故障恢复"
        elif data1 == '8' and data2 == 'B':
            return "隔离"
        elif data1 == '8' and data2 == 'C':
            return "释放"
        elif data1 == '9' and data2 == '0':
            return "手动启动"
        elif data1 == '9' and data2 == '1':
            return "手动启动撤销"
        elif data1 == '9' and data2 == '9':
            return "模板故障"
        elif data1 == '9' and data2 == 'A':
            return "模板正常"
        elif data1 == 'A' and data2 == '3':
            return "主电故障"
        elif data1 == 'A' and data2 == '4':
            return "主电恢复"
        elif data1 == 'A' and data2 == '5':
            return "备电故障"
        elif data1 == 'A' and data2 == '6':
            return "备电恢复"
            
    def returnitem(self,data1,data2):
        if data1 == '0' and data2 == '0':
            return "部件"
        elif data1 == '0' and data2 == '1':
            return "手报"
        elif data1 == '0' and data2 == '2':
            return "线型"
        elif data1 == '0' and data2 == '3':
            return "燃气"
        elif data1 == '0' and data2 == '4':
            return "感温"
        elif data1 == '0' and data2 == '5':
            return "控制"
        elif data1 == '0' and data2 == '6':
            return "消泵"
        elif data1 == '0' and data2 == '7':
            return "一氧"
        elif data1 == '0' and data2 == '8':
            return "消报"
        elif data1 == '0' and data2 == '9':
            return "输入"
        elif data1 == '0' and data2 == 'A':
            return "模块"
        elif data1 == '0' and data2 == 'B':
            return "感烟"
        elif data1 == '0' and data2 == 'C':
            return "监视"
        elif data1 == '0' and data2 == 'D':
            return "声光"
        elif data1 == '0' and data2 == 'E':
            return "广播"
        elif data1 == '0' and data2 == 'F':
            return "中继"
        elif data1 == '1' and data2 == '0':
            return "电源"
        elif data1 == '1' and data2 == '1':
            return "回路"
        elif data1 == '1' and data2 == '2':
            return "多线"
        elif data1 == '1' and data2 == '3':
            return "层显"
        elif data1 == '1' and data2 == '4':
            return "总线"
        elif data1 == '1' and data2 == '5':
            return "系统"
        elif data1 == '1' and data2 == '6':
            return "通讯"
        elif data1 == '1' and data2 == '7':
            return "层显"
        elif data1 == '1' and data2 == '8':
            return "区域"
        elif data1 == '1' and data2 == '9':
            return "监视"
        elif data1 == '1' and data2 == 'A':
            return "LED"
        elif data1 == '1' and data2 == 'B':
            return "操作"
        elif data1 == '1' and data2 == 'C':
            return "存储"
       

if __name__=='__main__':
    socketserver.ThreadingTCPServer(("10.9.7.105",1221),Server).serve_forever()
