#-*- coding: utf-8 -*-
import socket,sys,os
import string,cgi,time

class Client(object):
    def __init__(self,HOST,PORT,CAMINHO):
        self.host=HOST
        self.port=PORT
        self.caminho = CAMINHO
    def startClient(self):
        try:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            dest = (socket.gethostbyname(self.host),self.port)

            tcp.connect(dest)
            print 'Conected'
            a = 'GET '+self.caminho+" HTTP/1.0\r\nUser-Agent: curl/7.16.3 libcurl/7.16.3 OpenSSL/0.9.7l zlib/1.2.3\r\nHost: "+self.host+"\r\nAccept-Language: pt-br\r\n\r\n"
            tcp.send(a)
            #RECEBENDO DADOS
            self.clientHttp(self.caminho,tcp)
            tcp.close()
            print 'Conection Closed'
        except:
            print 'Conection not efectuated'
    def end_file(self):

        aux1 = self.caminho
        aux = aux1.split('/')
        iteracao = len(aux)
        ends_file = aux[iteracao-1].split('.')
        tam = len(ends_file)
        if (tam == 2) and (ends_file != ''):
            arquivo = ends_file
            return ends_file[0]+'.'+ends_file[1]
        else:
            return 'index.html'
    def clientHttp(self,nomeArquivo,tcp):
        tipo = self.end_file()
        print tipo
        arquivo = open(tipo, 'w')
        #msn = tcp.recv((1048576))
        msn = tcp.recv(1048576)
        split= msn.split('\r\n\r\n')
        if split[0][9:12] == '200':
            print '\033[32m'+ split[0]+'\033[0;0m'
            arquivo.write(split[1])
        elif split[0][9:12] == '404':
            print '\033[31m'+ split[0]+'\033[0;0m'
            arquivo.write(split[1])
            print 'ERROR: 404 Page not Found'
        elif split[0][9:12] == '301':
            print '\033[33m'+ split[0]+'\033[0;0m'
            arquivo.write(split[1])
            print 'ERROR: 301 Moved Permanently'
        elif split[0][9:12] == '400':
            print '\033[32m'+ split[0]+'\033[0;0m'
            arquivo.write(split[1])
            print 'ERROR: 400 Bad Request'
        else:
            print '\033[33m'+ split[0]+'\033[0;0m'
            arquivo.write(split[1])
            print 'Some ERROR that is not in the list of errors: ',msn[9:12]
        arquivo.close()



if __name__ == "__main__":

    try:

        http_protocol = sys.argv[1].split('/',1)
        ca= "/"+http_protocol[1]
        client = Client(http_protocol[0],int(sys.argv[2]),ca)
        client.startClient()
    except:
        #https = 443
        print 'Port not informated'
        http_protocol = sys.argv[1].split('://')
        print http_protocol
        if http_protocol[0] == 'https':

            url = http_protocol[1].split('/',1)
            ca = "/"+url[1]
            client = Client(url[0],8443,ca)
            client.startClient()
        elif http_protocol[0] == 'http':

            url = http_protocol[1].split('/',1)
            ca = "/"+url[1]
            client = Client(url[0],80,ca)
            client.startClient()
