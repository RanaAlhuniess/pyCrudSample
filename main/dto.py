class DTO:
    def __init__(self, id_):
        self._id = id_

    @property
    def id(self):
        return self._id

class CustomerDTO(DTO):
    def __init__(self, id_, email, first_name,last_name, birthday, creator, grade):
        super().__init__(id_)
        self._email = email
        self._first_name = first_name
        self._last_name = last_name
        self._birthday = birthday
        self._creator = creator
        self._grade = grade