class Constants(object):
    END_LINE = b'\r\n'
    MAXIMUM_TTL = 60*60*24*30


class Commands(object):
    SET = b'set'
    GET = b'get'
    END_GET = b'END'
    STATS = b'stats'


class Errors(object):
    ERROR = b'ERROR'
    CLIENT_ERROR = b'CLIENT_ERROR'
    SERVER_ERROR = b'SERVER_ERROR'


class StoreReply(object):
    STORED = b'STORED'
    NOT_STORED = b'NOT_STORED'
    EXISTS = b'EXISTS'
    NOT_FOUND = b'NOT_FOUND'

