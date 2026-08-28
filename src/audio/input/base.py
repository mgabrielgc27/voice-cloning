from abc import ABC, abstractmethod

class AudioInput(ABC):
    
    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def read(self) -> bytes:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass