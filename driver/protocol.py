class Constants(object):
    END_LINE = b'\r\n'
    MAXIMUM_TTL = 60*60*24*30


class Commands(object):
    SET = b'set'
    GET = b'get'
    END_GET = b'END'
    STATS = b'stats'


class Errors(object):
    ERROR = 'ERROR'
    CLIENT_ERROR = 'CLIENT_ERROR'
    SERVER_ERROR = 'SERVER_ERROR'


class StoreReply(object):
    STORED = 'STORED'
    NOT_STORED = 'NOT_STORED'
    EXISTS = 'EXISTS'
    NOT_FOUND = 'NOT_FOUND'

