class DTO:
    def __init__(self, id_):
        self._id = id_

    @property
    def id(self):
        return self._id


class EmployeeDTO(DTO):
    def __init__(self, id_, birthday, creator, account):
        super().__init__(id_)
        self._birthday = birthday
        self._creator = creator
        self._account = account

    @property
    def birthday(self):
        return self._birthday

    @property
    def creator(self):
        return self._creator

    @property
    def account(self):
        return self._account

