class DTO:
    def __init__(self, id_):
        self._id = id_

    @property
    def id(self):
        return self._id


class CustomerDTO(DTO):
    def __init__(self, id_, email, first_name, last_name, nationality, birthday, creator, grade):
        super().__init__(id_)
        self._email = email
        self._first_name = first_name
        self._last_name = last_name
        self._nationality = nationality
        self._birthday = birthday
        self._creator = creator
        self._grade = grade

    @property
    def email(self):
        return self._email

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def nationality(self):
        return self._nationality

    @property
    def birthday(self):
        return self._birthday

    @property
    def creator(self):
        return self._creator

    @property
    def grade(self):
        return self._grade

