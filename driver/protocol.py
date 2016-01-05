END_LINE = "\r\n"


class Commands(object):
    SET = 'set'
    GET = 'get'
    END_GET = 'END'
    STATS = 'stats'


class Errors(object):
    ERROR = "ERROR"
    CLIENT_ERROR = "CLIENT_ERROR"
    SERVER_ERROR = "SERVER_ERROR"


class StoreReply(object):
    STORED = "STORED"
    NOT_STORED = "NOT_STORED"
    EXISTS = "EXISTS"
    NOT_FOUND = "NOT_FOUND"


