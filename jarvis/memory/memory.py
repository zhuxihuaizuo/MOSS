# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 下午2:43
# @Author  : Su Yang
# @File    : memory.py
# @Software: PyCharm 
# @Comment : base class for all memory class
import abc

from jarvis.singleton import AbstractSingleton


class Memory(AbstractSingleton):
    @abc.abstractmethod
    def add(self, data):
        pass

    @abc.abstractmethod
    def get(self, data):
        pass

    @abc.abstractmethod
    def clear(self):
        pass

    @abc.abstractmethod
    def get_relevant(self, data, num_relevant=5):
        pass

    @abc.abstractmethod
    def get_stats(self):
        pass
