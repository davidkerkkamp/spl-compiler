from enum import Enum, auto


class Register(Enum):
    PC = auto(),
    SP = auto(),
    MP = auto(),
    HP = auto(),
    RR = auto(),
    R5 = auto(),
    R6 = auto(),
    R7 = auto()

    def __str__(self):
        return {
            Register.PC: 'PC',
            Register.SP: 'SP',
            Register.MP: 'MP',
            Register.HP: 'HP',
            Register.RR: 'RR',
            Register.R5: 'R5',
            Register.R6: 'R6',
            Register.R7: 'R7',
        }.get(self)
