import socketserver
import MySQLdb
import struct
import time


class Server(socketserver.BaseRequestHandler):
    def __init__(self,request,client_address,server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.database = MySQLdb.connect("localhost","root","962424lgj","test",charset='utf8')
        print(self.client_address[0]+" connecting....")

        try:

            self.handle()
        finally:
            print(self.client_address[0]+" closing....")


    def handle(self):
        while True:
            #time.sleep(1)
            sk:socket.socket = self.request
            data = self.request.recv(1024)
            
            #查岗
            #db1 = MySQLdb.connect("localhost","root","962424lgj","CHECK",charset='utf8')
            #cursor1 = db1.cursor()
            #sql1= "select * from CheckOnline;"
            #sql2= "update CheckOnline set STATUS=\"0\";"
            #cursor1.execute(sql1)
            #for r in cursor1:
                #if r[0] == "1":
                    #print("OK")
                    #try:
                        #cursor1.execute(sql2);
                        #db1.commit()
                    #except:
                        #db1.rollback()                  
                    #sk.send("back".encode("utf-8"))#发送回复
            #db1.close()
            
            
            if not data: break
            print("******************************************************************************************************************************************************")
            print('->client:', data.hex())
            tmpdata = data.hex()
            if((tmpdata[0]=='4') and (tmpdata[1]=='0') and (tmpdata[2]=='4') and (tmpdata[3]=='0')):
                head,num,vertion,time,n1,n2,len1,len2,cmd=struct.unpack("!3H6s6s6s3B",data[:27])
                length=len2*256+len1
                head,num,vertion,time,n1,n2,len1,len2,cmd,msg,checksum,end=struct.unpack("!3H6s6s6s3B"+str(length)+"sHB",data[:(30+length)])
                mydata=msg.hex()
                print('->msg:', mydata)
                machinetype = returnmch((INT(mydata[0])*16+INT(mydata[1])))#获得机器类型
                print(machinetype)
            
                if((INT(mydata[0])*16+INT(mydata[1])) == 1):#主机状态
                    item = "本机状态"
                    huilu=""
                    addr = ""
                    #addr = INT(mydata[2])*16+mydata[3]
                    state = ReturnNewState_1(calcullate16bit(mydata[8],mydata[9],mydata[10],mydata[11])) 
                    pub_date = ReturnTime(mydata[12],mydata[13],mydata[14],mydata[15],mydata[16],mydata[17],mydata[18],mydata[19],mydata[20],mydata[21],mydata[22],mydata[23])
                elif((INT(mydata[0])*16+INT(mydata[1])) == 2):#部件状态
                    #item = ReturnNewItem_2(INT(mydata[8])*16+INT(mydata[9]))
                    #state = ReturnNewState_2(calcullate16bit(mydata[18],mydata[19],mydata[20],mydata[21]))
                    item = returnitem(mydata[8],mydata[9])
                    state = returnstate(mydata[20],mydata[21])
                    huilu = INT(mydata[10])*4096+INT(mydata[11])*256+INT(mydata[12])*16+INT(mydata[13])  
                    addr = INT(mydata[14])*4096+INT(mydata[15])*256+INT(mydata[16])*16+INT(mydata[17])
                    print("huilu->",str(huilu))
                    print("addr->",str(addr))  
                    #addr = calcullate16bit(mydata[10],mydata[11],mydata[12],mydata[13])
                    pub_date = ReturnTime(mydata[83],mydata[84],mydata[85],mydata[86],mydata[87],mydata[88],mydata[89],mydata[91],mydata[92],mydata[93],mydata[94],mydata[95])
                elif((INT(mydata[0])*16+INT(mydata[1])) == 4):#操作信息
                    item = "本机操作"
                    state = ReturnNewState_4(INT(mydata[8])*16+INT(mydata[9]))
                    huilu=""
                    addr = ""
                    pub_date = ReturnTime(mydata[12],mydata[13],mydata[14],mydata[15],mydata[16],mydata[17],mydata[18],mydata[19],mydata[20],mydata[21],mydata[22],mydata[23])
                elif((INT(mydata[0])*16+INT(mydata[1])) == 21):#部件状态
                    item = "本机状态"
                    state = ReturnNewState_21(INT(mydata[4])*16+INT(mydata[5]))
                    if state=="主电故障":
                        power=1
                    elif state=="备电故障":
                        power=2
                    
                    if state=="未定义" and power==1:
                        state="主电恢复"
                        power=0
                    elif state=="未定义" and power==3:
                        state="备电恢复"
                        power=0

                    addr = ""
                    huilu=""
                    pub_date = ReturnTime(mydata[6],mydata[7],mydata[8],mydata[9],mydata[10],mydata[11],mydata[12],mydata[13],mydata[14],mydata[15],mydata[16],mydata[17])
                elif((INT(mydata[0])*16+INT(mydata[1])) == 24):#用户信息传输装置操作信息
                    item = "本机操作"
                    state = ReturnNewState_24(INT(mydata[4])*16+INT(mydata[5]))
                    addr = ""
                    pub_date = ReturnTime(mydata[8],mydata[9],mydata[10],mydata[11],mydata[12],mydata[13],mydata[14],mydata[15],mydata[16],mydata[17],mydata[18],mydata[19])
                elif((INT(mydata[0])*16+INT(mydata[1])) == 28):#时间
                    item = "本机"
                    state = "时间上传"
                    addr = ""
                    huilu=""
                    pub_date = ReturnTime(mydata[4],mydata[5],mydata[6],mydata[7],mydata[8],mydata[9],mydata[10],mydata[11],mydata[12],mydata[13],mydata[14],mydata[15])
                else:
                    item = "未定义"
                    state="未定义"
                    addr=""
                    huilu=""
                    pub_date=time.now()
                
                if head == 0x4040:
                    cmd=3
                    senddata=struct.pack("!3H6s6s6s3B"+str(length)+"sHB",head,num,vertion,time,n1,n2,len1,len2,cmd,msg,checksum,end)
                    
                    
                    db1 = MySQLdb.connect("localhost","root","962424lgj","CHECK",charset='utf8')
                    cursor1 = db1.cursor()
                    sql1= "select * from CheckOnline;"
                    sql2= "update CheckOnline set STATUS=\"0\";"
                    cursor1.execute(sql1)
                    for r in cursor1:
                        if r[0] == "1":
                            print("OK")
                            try:
                                cursor1.execute(sql2);
                                db1.commit()
                            except:
                                db1.rollback()                  
                            sk.send("back".encode("utf-8"))#发送回复
                        else:
                            sk.send(senddata)
                    db1.close()
                
                    
                    if((INT(mydata[0])*16+INT(mydata[1])) != 28):
                        db = MySQLdb.connect("localhost","root","962424lgj","FireData",charset='utf8')
                        cursor = db.cursor()
                        sql = "INSERT INTO Data (device,item,huilu,addr,state,pub_date) VALUES("+"\""+str(machinetype)+"\",\""+str(item)+"\",\""+str(huilu)+"\",\""+str(addr)+"\",\""+str(state)+"\",\""+str(pub_date)+"\");"
                        print(sql)
                        try:
                            print("execute ok")
                            cursor.execute(sql)
                            db.commit()
                        except:
                            db.rollback()
                        db.close()
                        print("close ok")
                    
        self.request.close()

def ReturnTime(d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12):
    time = ""
    time ="20"+str(INT(d11)*16+INT(d12))+"-"+str(INT(d9)*16+INT(d10))+"-"+str(INT(d7)*16+INT(d8))+" "+str(INT(d5)*16+INT(d6))+":"+str(INT(d3)*16+INT(d4))+":"+str(INT(d1)*16+INT(d2))
    return time

def ReturnNewState_1(data):#类型1的状态处理
    if(data&0x0002 == 0x0002):
        return "火警"
    elif(data&0x0004 == 0x0004):
        if(data&0x0100 == 0x0100):
            return "主电故障"
        elif(data&0x0200 == 0x0200):
            return "备电故障"
        elif(data&0x0400 == 0x0400):
            return "总线故障"
        else:
            return "故障"
    elif(data&0x0008 == 0x0008):
        return "屏蔽"
    elif(data&0x0010 == 0x0010):
        return "监管"
    elif(data&0x0020 == 0x0020):
        return "启动"
    elif(data&0x0040 == 0x0040):
        return "反馈"
    elif(data&0x0080 == 0x0080):
        return "延时"
    elif(data&0x0800 == 0x0800):
        return "手动状态"
    elif(data&0x1000 == 0x1000):
        return "配置改变"
    elif(data&0x2000 == 0x2000):
        return "复位"
    elif(data&0x0100 == 0x0100):
        return "主电故障"
    elif(data&0x0200 == 0x0200):
        return "备电故障"
    elif(data&0x0400 == 0x0400):
        return "总线故障"
    else:
        return "未定义"

def ReturnNewState_2(data):
    if(data&0x0002 == 0x0002):
        return "火警"
    elif(data&0x0004 == 0x0004):
        if(data&0x0800 == 0x0800):
            return "电源故障"
        else:
            return "故障"
        
    elif(data&0x0008 == 0x0008):
        return "屏蔽"
    elif(data&0x0010 == 0x0010):
        return "监管"
    elif(data&0x0020 == 0x0020):
        return "启动"
    elif(data&0x0040 == 0x0040):
        return "反馈"
    elif(data&0x0080 == 0x0080):
        return "延时"
    elif(data&0x0800 == 0x0800):
        return "电源故障"
    elif(data&0x0004 == 0x0004):
        return "故障"
    else:
        return "未定义"
    
def ReturnNewItem_2(data):#部件类型解析
    if(data==1):
        return "火灾报警控制器"
    elif(data == 10):
        return "可燃气体探铡器"
    elif(data == 21):
        return "探测回路"
    elif(data == 22):
        return "火灾显示盘"
    elif(data == 23):
        return "手动火灾报警按钮"
    elif(data == 24):
        return "消火栓按钮"
    elif(data == 25):
        return "火灾探测器"
    elif(data == 30):
        return "感温火灾探测器"
    elif(data == 40):
        return "感烟火灾探测器"
    elif(data == 61):
        return "紫外火焰探测器"
    elif(data == 62):
        return "红外火焰探测器"
    elif(data == 69):
        return "感光火灾探测器"
    elif(data == 74):
        return "气体探测器"
    elif(data == 79):
        return "感声火灾探测器"
    elif(data == 81):
        return "气体灭火控制器"
    elif(data == 82):
        return "消防电气控制装置"
    elif(data == 83):
        return "消防控制室图形显示装置"
    elif(data == 84):
        return "模块"
    elif(data == 85):
        return "输入模块"
    elif(data == 86):
        return "输出模块"
    elif(data == 87):
        return "输入／输出模块"
    elif(data == 88):
        return "中继模块"
    elif(data == 91):
        return "消防水泵"
    elif(data == 92):
        return "消防水箱"
    elif(data == 95):
        return "喷淋泵"
    elif(data == 99):
        return "压力开关"
    elif(data == 102):
        return "防火门"
    elif(data == 103):
        return "防火阀"
    elif(data == 117):
        return "防火阀"
    elif(data == 118):
        return "防火门监控器"
    elif(data == 121):
        return "警报装置"
    else:
        return "未定义"

def ReturnNewState_4(data):#主机操作状态
    if(data == 1):
        return "复位"
    elif(data == 2):
        return "消音"
    elif(data == 4):
        return "手动报警"
    elif(data == 8):
        return "警情消除"
    elif(data == 16):
        return "自检"
    elif(data == 32):
        return "确认"
    elif(data == 64):
        return "测试"
    else:
        return "未定义"

def ReturnNewState_21(data):#用传状态
    if(data == 3):
        return "火警"
    elif(data == 5):
        return "故障"
    elif(data == 9):
        return "主电故障"
    elif(data == 17):
        return "备电故障"
    elif(data == 33):
        return "与监控中心通信信道故障"
    elif(data == 65):
        return "监涮连接线路故障"
    else:
        return "未定义"

def ReturnNewState_24(data):#用传操作
    if(data == 1):
        return "复位"
    elif(data == 2):
        return "消音"
    elif(data == 4):
        return "手动报警"
    elif(data == 8):
        return "警情消除"
    elif(data == 16):
        return "自检"
    elif(data == 32):
        return "查岗应答"
    elif(data == 64):
        return "测试"
    else:
        return "未定义"

def calcullate16bit(d1,d2,d3,d4):#转16位数字
    return (INT(d4)*4096+INT(d3)*256+INT(d2)*16+INT(d1))

def returnstate(data1,data2):
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

def returnitem(data1,data2):
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

def returnMsgtype(data1,data2):
    if((data1 == '0') and (data2 == '1')):
        return 1
    elif((data1 == '0') and (data2 == '2')):
        return 2
    elif((data1 == '0') and (data2 == '4')):
        return 4
    elif((data1 == '1') and (data2 == '5')):
        return 21
    elif((data1 == '1') and (data2 == '8')):
        return 24
    elif((data1 == '1') and (data2 == 'C')):
        return 28

def returnmch(data):
    if((data == 1)or(data == 2)or(data == 4)):
        return "消防主机"
    elif((data == 21)or(data == 28)or(data == 24)):
        return "用户信息传输装置"
        

def INT(data):
    if(data == "F"):
        return 15
    elif(data == "E"):
        return 14
    elif(data == "D"):
        return 13
    elif(data == "C"):
        return 12
    elif(data == "B"):
        return 11
    elif(data == "A"):
        return 10
    else:
        return int(data,16) 
        

if __name__=='__main__':
    socketserver.ThreadingTCPServer(("10.9.7.105",1221),Server).serve_forever()
