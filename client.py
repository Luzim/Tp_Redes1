#-*- coding: utf-8 -*-
import socket,sys,os


class Client(object):
    def __init__(self,HOST,PORT):
        self.host=HOST
        self.port=PORT
    def startClient(self):
        try:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dest = (self.host,self.port)
            tcp.connect(dest)
            msn = tcp.recv(1024)
            print msn
            msg = raw_input()
            tcp.send (msg)
            partofMessege = msg.split(' ')
            nome_arq =partofMessege[1].split('/')

            #RECEBENDO DADOS
            msn = tcp.recv(1024)
            print msn
            msn = tcp.recv(1024)
            print msn
            if msn is 200:
                self.clientHttp(nome_arq[1],tcp)
            else:
                msn = tcp.recv(102400)
                print msn
                msn = tcp.recv(102400)
                print msn
            tcp.close()
            print 'Conection Closed'
        except:
            print 'Conection not efectuated'
    def clientHttp(self,nomeArquivo,tcp):
        msn = tcp.recv(102400)
        print msn
        msn = tcp.recv(102400)
        print msn
        arquivo = open(nomeArquivo, 'w')
        arquivo.write(msn)
        arquivo.close()


if __name__ == "__main__":

    try:
        client = Client(sys.argv[1],int(sys.argv[2]))
        client.startClient()
    except:
        print 'Port not informated'
        client = Client(sys.argv[1],8080)
        client.startClient()
