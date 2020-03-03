from abc import ABCMeta, abstractmethod, abstractproperty


class BaseScheduler(metaclass=ABCMeta):

    @abstractmethod
    async def execute(self):
        """Extract data from job"""
