from __future__ import print_function
import sys
from twisted.internet import defer, endpoints, protocol, ssl, task

certificate = ssl.Certificate.loadPEM(
    open("../../../examples/server.pem").read()
)

def main(reactor, host, port=443):
    contextFactory = ssl.CertificateOptions(trustRoot=certificate,
                                            hostname=host.decode("utf-8"))
    port = int(port)
    done = defer.Deferred()

    class ShowCertificate(protocol.Protocol):
        def connectionMade(self):
            self.transport.write(b"GET / HTTP/1.0\r\n\r\n")
        def dataReceived(self, data):
            certificate = ssl.Certificate(self.transport.getPeerCertificate())
            print(certificate)
            self.transport.loseConnection()
        def connectionLost(self, reason):
            if reason.check(ssl.SSL.Error):
                print(reason.value)
            done.callback(None)

    endpoints.connectProtocol(
        endpoints.SSL4ClientEndpoint(reactor, host, port,
                                     sslContextFactory=contextFactory),
        ShowCertificate()
    )
    return done

task.react(main, sys.argv[1:])
