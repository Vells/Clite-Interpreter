# coding=utf-8
__author__ = 'vdmine11'


# Define our own domain of values
class CliteValue(object):
    """
    A Base Clite value class
    """
    pass


class IntValue(CliteValue):
    """
    Implement Integers however you want for Clite
    """

    def __init__(self, value):
        """
        Convert a Python v integer into some kind of
        Clite integer
        :param value:
        :return:
        """
        self.value = value


class FloatValue(CliteValue):
    pass


class BoolValue(CliteValue):
    pass


class StructValue(CliteValue):
    pass