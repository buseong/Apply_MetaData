class SearchError(Exception):
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.msg


class GetSoupError(SearchError):
    pass


class GetInfoError(Exception):
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.msg


class AlreadyExistsError(SearchError):
    pass
