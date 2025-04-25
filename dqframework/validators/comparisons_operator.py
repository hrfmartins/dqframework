import enum

class ComparisonsOperator(enum.Enum):
    EQUAL = '=='
    NOT_EQUAL = '!='
    GREATER = '>'
    LESS = '<'
    GREATER_EQUAL = '>='
    LESS_EQUAL = '<='

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.name
