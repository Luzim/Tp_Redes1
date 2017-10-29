#-*- coding: utf-8 -*-
import socket
import os
import sys
from netifaces import interfaces, ifaddresses, AF_INET
class SimpleHTTP(object):
    def _doGET(self,objeto,caminho,con):
        try:
            if objeto == '/':
                f=open(caminho+'/index.html','r')
                aux =f.read()
                response_headers = {
                'Content-Type': 'html; encoding=utf8',
                'Content-Length': len(aux),
                'Connection': 'close',
                }
                response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.iteritems())
                response_proto = '\nHTTP/1.1'
                response_status = 200
                response_status_text = ' OK'
                con.send('%s %s %s'%(response_proto,response_status,response_status_text)+'\n'+response_headers_raw+'\r\n'+aux)
            else:
                f=open(caminho+objeto,'r')
                aux =f.read()
                response_headers = {
                'Content-Type': 'html; encoding=utf8',
                'Content-Length': len(aux),
                'Connection': 'close',
                }
                response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.iteritems())
                response_proto = '\nHTTP/1.1'
                response_status = 200
                response_status_text = ' OK'
                con.send('%s %s %s'%(response_proto,response_status,response_status_text)+'\n'+response_headers_raw+'\r\n'+aux)
        except IOError:
            response_proto = '\nHTTP/1.1'
            response_status = 404
            response_status_text = ' File not Found'

            f=open(caminho+'/404ERROR.html','r')
            aux =f.read()
            response_headers = {
            'Content-Type': 'html; encoding=utf8',
            'Content-Length': len(aux),
            'Connection': 'close',
            }
            response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.iteritems())
            con.send('%s %s %s' % (response_proto, response_status,response_status_text)+'\n'+response_headers_raw+'\r\n'+aux)

class Server(SimpleHTTP):
    def __init__(self,HOST,PORT):
        self.host=HOST
        self.port=PORT
    def _doGET(self,arg1,arg2,arg3):
        SimpleHTTP._doGET(self,arg1,arg2,arg3)
    def startServer(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        orig = (self.host,self.port)
        tcp.bind(orig)
        tcp.listen(1)
        while True:
            con, cliente = tcp.accept()
            pid = os.fork()
            if pid == 0:
                tcp.close()
                print 'Conected by', cliente
                msg = con.recv(1048576)
                if not msg: break
                print cliente, msg
                nomeArquivo=msg.split(' ')
                print 'Nome arquivo ',nomeArquivo[1]
                if nomeArquivo[0] == "GET":
                    self._doGET(nomeArquivo[1],DocumentRoot,con)
                else:
                    con.send('Comando GET nao solicitado\n')
                print 'Finalizando conexao do cliente', cliente
                con.close()
                sys.exit(0)
            else:
                con.close()
if __name__ == "__main__":
    DocumentRoot = "%s/arquivos" % os.path.realpath(os.path.dirname(__file__))
    try:
        server = Server(sys.argv[1],int(sys.argv[2]))
        server.startServer()
    except:
        print 'Port not informated - 8080'
        for ifaceName in interfaces():
            addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
        print addresses
        server = Server(addresses[0], 8080)

        server.startServer()
