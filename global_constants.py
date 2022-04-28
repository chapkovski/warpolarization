from enum import Enum


class strEnum(str, Enum):
    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class POSITION(strEnum):
    YES = 'yes'
    NO = 'no'
    NR = 'nr'


class ROLE(strEnum):
    DICTATOR = 'dictator'
    RECIPIENT = 'recipient'


class TREATMENT(strEnum):
    BASELINE = 'baseline'
    VL = 'vl'  # voluntarily reveal by recipient
    FR = 'forced_reveal'  # recipient position revealed to Dictator involuntarily by an experimenter
    RB = 'reveal_before'  # recipient position revealed by Dictator
