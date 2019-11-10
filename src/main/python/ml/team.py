class Team:
    def __init__(self, members):
        self.__members = members

    def __len__(self):
        return len(self.__members)

    def __contains__(self, member):
        return member in self.__members
