from abc import ABC
import abc

class Bird(ABC):

    @abc.abstractmethod
    def fly(self):
        pass
