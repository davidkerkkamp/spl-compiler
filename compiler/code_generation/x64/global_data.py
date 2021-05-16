from enum import Enum, auto


class DataType(Enum):
    resb = auto(),  # 8-bit
    resw = auto(),  # 16-bit
    resd = auto(),  # 32-bit
    resq = auto(),  # 64-bit
    resdq = auto(),  # 128-bit

    def __str__(self):
        return self.name


# Variable declared in .bss section
class BssVariable:
    def __init__(self, id: int, size: DataType = DataType.resq, count: int = 1):
        self.id = id
        self.name = f'global_{id}'
        self.size = size
        self.count = count

    def __str__(self):
        return f'{self.name}:    {self.size}    {self.count}'
