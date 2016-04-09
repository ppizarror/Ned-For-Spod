# urllib2 work-alike interface
# ...from urllib2...
import httplib
from urllib2 import \
     URLError, \
     HTTPError

from _auth import \
     HTTPProxyPasswordMgr, \
     HTTPSClientCertMgr
from _debug import \
     HTTPResponseDebugProcessor, \
     HTTPRedirectDebugProcessor
from _http import \
     HTTPEquivProcessor, \
     HTTPRefererProcessor, \
     HTTPRefreshProcessor, \
     HTTPRobotRulesProcessor, \
     RobotExclusionError
from _opener import OpenerDirector, \
     SeekableResponseOpener, \
     build_opener, install_opener, urlopen
from _request import \
     Request
from _urllib2_fork import \
     AbstractBasicAuthHandler, \
     AbstractDigestAuthHandler, \
     BaseHandler, \
     CacheFTPHandler, \
     FileHandler, \
     FTPHandler, \
     HTTPBasicAuthHandler, \
     HTTPCookieProcessor, \
     HTTPDefaultErrorHandler, \
     HTTPDigestAuthHandler, \
     HTTPErrorProcessor, \
     HTTPHandler, \
     HTTPPasswordMgr, \
     HTTPPasswordMgrWithDefaultRealm, \
     HTTPRedirectHandler, \
     ProxyBasicAuthHandler, \
     ProxyDigestAuthHandler, \
     ProxyHandler, \
     UnknownHandler


# ...and from mechanize
# crap ATM
## from _gzip import \
##      HTTPGzipProcessor
if hasattr(httplib, 'HTTPS'):
    from _urllib2_fork import HTTPSHandler
del httplib
