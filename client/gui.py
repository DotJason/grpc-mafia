from abc import ABC, abstractmethod


class GUI:
    @abstractmethod
    def log(self, s):
        raise NotImplementedError

    @abstractmethod
    def log_buffer(self, s):
        raise NotImplementedError
