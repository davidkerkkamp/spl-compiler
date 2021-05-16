from abc import abstractmethod, ABC
from typing import List

from compiler.compiler_warnings import CompilerWarning


class ReturnValueAnalyzable(ABC):
    @abstractmethod
    def all_paths_return(self, warnings: List[CompilerWarning]) -> (bool, bool):
        return False