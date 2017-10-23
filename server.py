#-*- coding: utf-8 -*-
import socket
import os
import sys

class SimpleHTTP(object):
    def _doGET(self,objeto,caminho,con):
        try:
            f=open(caminho+objeto)
            aux =f.read()
            response_headers = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': len(aux),
            'Connection': 'close',
            }
            response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.iteritems())
            response_proto = '\nHTTP/1.1'
            response_status = 200
            response_status_text = 'OK'

            con.send('%s %s %s' % (response_proto, response_status,response_status_text))
            con.send('\n')
            con.send(response_headers_raw)
            con.send(aux)

        except IOError:
            response_proto = 'HTTP/1.1'
            response_status = 404
            response_status_text = 'File not Found'

            con.send('%s %s %s' % (response_proto, response_status,response_status_text))
            print ('%s %s %s' % (response_proto, response_status,response_status_text))
            '''
            con.send('%s'%response_proto+'\n')
            con.send('%s'%response_status+'\n')
            con.send('%s'%response_status_text+'\n')
            con.send('\n')
            '''
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
                msn = 'Conected (HOST: '+self.host+' PORT: '+str(self.port)+')\n'
                con.send(msn)
                msg = con.recv(1024)
                if not msg: break
                print cliente, msg
                nomeArquivo=msg.split(' ')
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
    DocumentRoot = "%s/arquivos/" % os.path.realpath(os.path.dirname(__file__))
    try:
        server = Server(sys.argv[1],int(sys.argv[2]))
        server.startServer()
    except:
        server = Server('localhost', 8080)
        server.startServer()
