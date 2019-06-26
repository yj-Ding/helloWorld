import socket
import threading
import sys
import os
import tensorflow as tf
import matplotlib.image as img
# 创建 socket 对象

filename1=""
def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 9999))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print ('Waiting connection...')

    conn, addr = s.accept()
    print("已连接",addr)
    t = threading.Thread(target=deal_data, args=(conn, addr))
    t.start()


def deal_data(conn, addr):
    print ('Accept new connection from {0}'.format(addr))
    #conn.settimeout(500)
    conn.send((bytes)('Hi, Welcome to the server!'.encode("utf-8")))
    msg=conn.recv(1024).decode('utf-8')



    while 1:

        if msg:
            m = msg.split(',')
            filename = m[0]
            filesize = int(m[1])

            new_filename = os.path.join('./', filename + ".png")
            filename1=new_filename
            print('file new name is {0}, filesize is {1}'.format(new_filename,
                                                                 filesize))

            recvd_size = 0  # 定义已接收文件的大小
            fp = open(new_filename, 'wb')
            print('start receiving...')
            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                    print(recvd_size,"/",filesize)
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print ('end receive...')
        break
    model=tf.keras.models.load_model('cnn_mnist.model')
    print("name:",new_filename)
    new_filename.replace('./','')
    mytest=img.imread(new_filename)
    my_test=mytest.reshape(1,28,28,1).astype('float32')
    prediction=model.predict_classes(my_test)
    
    print(prediction)
    word='the prediction is{0}'.format(prediction)
    
    conn.send((bytes)(word.encode("utf-8")))
    print(word)
    conn.close()
        
if __name__ == '__main__':
    socket_service()