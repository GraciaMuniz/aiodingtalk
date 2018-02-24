
class DingTalkTimeoutError(Exception):
    pass


class DingTalkError(Exception):

    def __init__(self, errcode=None, errmsg=None):
        self.errcode = errcode
        self.errmsg = errmsg
