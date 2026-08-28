from abc import ABC, abstractmethod

class AudioOutput(ABC):

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def write(self, data: bytes) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass