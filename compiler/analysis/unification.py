from __future__ import annotations
from typing import Dict, List

import compiler.errors as err
from compiler.utils import CodeRange


class UnificationError(Exception):
    def __init__(self, t1: InferenceType, t2: InferenceType):
        self.t1 = t1
        self.t2 = t2


class TypeRecursionError(Exception):
    def __init__(self, tv: int, other: InferenceType):
        self.tv = tv
        self.other = other


class Subst:
    def __init__(self, substitutions: Dict[int, InferenceType]):
        self.substitutions: Dict[int, InferenceType] = substitutions

    @classmethod
    def empty(cls):
        return cls(dict())

    @classmethod
    def single(cls, num: int, replacement: InferenceType):
        return cls({num: replacement})

    def compose(self, other: Subst):
        return Subst({
            **{i: v.substitute(self) for (i, v) in other.substitutions.items()},
            **{i: v.substitute(self) for (i, v) in self.substitutions.items()}
        })

    def get(self, num: int):
        return self.substitutions.get(num, InferenceTypeVar(num))


# Method implementations in this base class are used for basic types int, char, bool and void
class InferenceType:
    def unify(self, other: InferenceType):
        if other.is_type_var():
            return other.unify(self)

        if self.is_equal(other):
            return Subst.empty()
        else:
            raise UnificationError(self, other)

    def unify_or_type_error(self, other: InferenceType, code_range: CodeRange):
        try:
            return self.unify(other)
        except UnificationError as e:
            raise err.TypeMismatch(code_range, self, other)
        except TypeRecursionError as e:
            raise err.InvalidTypeError(code_range, e.tv, e.other)

    def is_type_var(self):
        return isinstance(self, InferenceTypeVar)

    def is_scalar(self):
        return isinstance(self, InferenceInt) or isinstance(self, InferenceChar) or isinstance(self, InferenceBool)

    def contains_typevar(self, num: int):
        return False

    def is_equal(self, other):
        return self.__class__ == other.__class__

    def substitute(self, subst: Subst):
        return self

    def collect_type_vars(self, result: List[int]) -> List[int]:
        return result


# *************************** Basic inference types ***************************
class InferenceInt(InferenceType):
    def __str__(self):
        return 'int'


class InferenceChar(InferenceType):
    def __str__(self):
        return 'char'


class InferenceBool(InferenceType):
    def __str__(self):
        return 'bool'


class InferenceVoid(InferenceType):
    def __str__(self):
        return 'void'


# *************************** Tuple inference type ***************************
class InferenceTuple(InferenceType):
    def __init__(self, t1: InferenceType, t2: InferenceType):
        self.t1 = t1
        self.t2 = t2

    def unify(self, other: InferenceType):
        if other.is_type_var():
            return other.unify(self)
        if self.is_equal(other):
            return Subst.empty()

        if isinstance(other, InferenceTuple):
            star = self.t1.unify(other.t1)
            return self.t2.substitute(star).unify(other.t2).compose(star)
        else:
            raise UnificationError(self, other)

    def is_equal(self, other):
        if isinstance(other, InferenceTuple):
            return self.t1.is_equal(other.t1) and self.t2.is_equal(other.t2)
        else:
            return False

    def contains_typevar(self, num: int):
        return self.t1.contains_typevar(num) or self.t2.contains_typevar(num)

    def substitute(self, subst: Subst):
        return InferenceTuple(self.t1.substitute(subst), self.t2.substitute(subst))

    def collect_type_vars(self, result: List[int]):
        result = self.t1.collect_type_vars(result)
        return self.t2.collect_type_vars(result)

    def __str__(self):
        return f'({str(self.t1)}, {str(self.t2)})'


# *************************** Tuple inference type ***************************
class InferenceList(InferenceType):
    def __init__(self, t: InferenceType):
        self.t = t

    def unify(self, other: InferenceType):
        if other.is_type_var():
            return other.unify(self)
        if self.is_equal(other):
            return Subst.empty()

        if isinstance(other, InferenceList):
            return self.t.unify(other.t)
        else:
            raise UnificationError(self, other)

    def is_equal(self, other):
        if isinstance(other, InferenceList):
            return self.t.is_equal(other.t)
        else:
            return False

    def contains_typevar(self, num: int):
        return self.t.contains_typevar(num)

    def substitute(self, subst: Subst):
        return InferenceList(self.t.substitute(subst))

    def collect_type_vars(self, result: List[int]):
        return self.t.collect_type_vars(result)

    def __str__(self):
        return f'[{str(self.t)}]'


# *************************** Type variable inference type ***************************
class InferenceTypeVar(InferenceType):
    def __init__(self, num: int):
        self.num = num

    def unify(self, other: InferenceType):
        if self.is_equal(other):
            return Subst.empty()

        if other.contains_typevar(self.num):
            raise TypeRecursionError(self.num, other)
        else:
            return Subst.single(self.num, other)

    def is_equal(self, other):
        if isinstance(other, InferenceTypeVar):
            return self.num == other.num
        else:
            return False

    def contains_typevar(self, num: int):
        if num is None:
            return True
        return num == self.num

    def substitute(self, subst: Subst):
        return subst.get(self.num)

    def collect_type_vars(self, result: List[int]):
        result.append(self.num)
        return result

    def __str__(self):
        return f'v{self.num}'
