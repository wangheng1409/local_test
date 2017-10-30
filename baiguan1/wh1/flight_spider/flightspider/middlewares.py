from twisted.web._newclient import ResponseNeverReceived
from twisted.internet.error import TimeoutError, ConnectionRefusedError, ConnectError
from flightspider import database


class CustomRedirectMiddleware(object):
    """Handle redirection of requests based on response status and meta-refresh html tag"""
    DONT_RETRY_ERRORS = (TimeoutError, ConnectionRefusedError, ResponseNeverReceived, ConnectError, ValueError)

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.DONT_RETRY_ERRORS):
            if spider.hp_id>0:
                sql = "UPDATE http_proxy SET state=%s WHERE id=%s" % (4, spider.hp_id)
                database.db.update(sql)
            spider.CloseSpider()
        print "exception =========================" + request.date


def process_request(self, request, spider):
    print "request  ======== " + request.url


def process_response(self, request, response, spider):

    print response.status, type(response.status)
    print "response ================="
    return response
