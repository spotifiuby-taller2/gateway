class SpotifiubiException(Exception):
    def __init__(self, status_code, detail):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


class Case1Exception(SpotifiubiException):
    def __init__(self):
        msg = "message 1"
        super().__init__(status_code=400, detail=msg)


class Case2Exception(SpotifiubiException):
    def __init__(self):
        msg = "message 2"
        super().__init__(status_code=400, detail=msg)


class Case3Exception(SpotifiubiException):
    def __init__(self):
        msg = "message 3"
        super().__init__(status_code=400, detail=msg)