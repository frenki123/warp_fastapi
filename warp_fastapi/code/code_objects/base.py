from abc import ABC, abstractmethod
from typing import Any

from ...main import AppObject
from ..config import NameConfig
from ..utils import ident_text


class AbstractVariableCode(ABC):
    name: str
    type: str | None = None
    value: str | None = None

    @abstractmethod
    def __init__(self, **kwargs: dict[str, Any]):
        pass  # pragma: no cover

    def __str__(self) -> str:
        res = self.name
        if self.type:
            res += f': {self.type}'
        if self.value:
            res += f' = {self.value}'
        return res.strip('\n')

    def __repr__(self) -> str:
        return self.__str__()  # pragma: no cover

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, AbstractVariableCode):
            return str(AbstractVariableCode) == str(AbstractVariableCode)
        return False

    def __hash__(self) -> int:
        return hash(str(self))  # pragma: no cover

    def add_optional(self) -> None:
        if self.type:
            self.type += ' | None'
        else:
            raise ValueError("Attribute doesn't have a type!")


class SimpleVariable(AbstractVariableCode):
    def __init__(self, name: str, type: str | None = None, value: str | None = None):
        self.name = name
        self.type = type
        self.value = value


class AbstractDecoratorCode(ABC):
    name: str
    params: list[AbstractVariableCode] = []
    is_function: bool = False

    @abstractmethod
    def __init__(self, **kwargs: dict[str, Any]):
        pass  # pragma: no cover

    def __str__(self) -> str:
        if self.params:
            params = [str(param) for param in self.params]
            return f"@{self.name}({', '.join(params)})"
        if self.is_function:
            return f'@{self.name}()'
        return f'@{self.name}'.strip('\n')

    def __repr__(self) -> str:
        return str(self)  # pragma: no cover


class SimpleDecoratorCode(AbstractDecoratorCode):
    def __init__(self, name: str, params: list[AbstractVariableCode] = [], is_function: bool = False):
        self.name = name
        self.params = params
        self.is_function = is_function


class AbstractFunctionCode(ABC):
    name: str
    content: str
    parametars: list[AbstractVariableCode] = []
    return_value: str | None = None
    decorators: list[AbstractDecoratorCode] = []

    @abstractmethod
    def __init__(self, **kwargs: dict[str, Any]):
        pass  # pragma: no cover

    def __str__(self) -> str:
        func_name = self.name
        params = ''
        return_val = ''
        decorators = ''
        if self.parametars:
            params = ', '.join([str(param) for param in self.parametars])
        if self.return_value:
            return_val = f' -> {self.return_value}'
        if self.decorators:
            decorators = '\n'.join([str(decorator) for decorator in self.decorators])
        return f"""{decorators}
def {func_name}({params}){return_val}:
{ident_text(self.content, 1)}
""".strip(
            '\n'
        )


class SimpleFunctionCode(AbstractFunctionCode):
    def __init__(
        self,
        name: str,
        content: str,
        parametars: list[AbstractVariableCode] = [],
        return_value: str | None = None,
        decorators: list[AbstractDecoratorCode] = [],
    ):
        self.name = name
        self.content = content
        self.parametars = parametars
        self.return_value = return_value
        self.decorators = decorators


class AbstractClassCode(ABC):
    class_name: str
    super_class_name: str | None = None
    attributes: list[AbstractVariableCode] = []
    methods: list[AbstractFunctionCode] = []

    @abstractmethod
    def __init__(self, **kwargs: dict[str, Any]):
        pass  # pragma: no cover

    def __str__(self) -> str:
        class_def = f'class {self.class_name}'
        if self.super_class_name:
            class_def += f'({self.super_class_name})'
        attributes = '\n'.join([str(att) for att in self.attributes])
        methods = '\n'.join([str(meth) for meth in self.methods])

        return f"""{class_def}:
{ident_text("pass",1) if not self.attributes and not self.methods else ""}
{ident_text(attributes,1)}
{ident_text(methods,1)}
""".strip(
            '\n'
        )


class SimpleClassCode(AbstractClassCode):
    def __init__(
        self,
        class_name: str,
        super_class_name: str | None = None,
        attributes: list[AbstractVariableCode] = [],
        methods: list[AbstractFunctionCode] = [],
    ):
        self.class_name = class_name
        self.super_class_name = super_class_name
        self.attributes = attributes
        self.methods = methods


class AbstractModuleCode(ABC):
    folder: str
    filename: str
    config: NameConfig
    imports: dict[str, set[str]] = {}
    type_checking_imports: dict[str, set[str]] = {}
    classes: list[AbstractClassCode] = []
    functions: list[AbstractFunctionCode] = []
    variables: list[AbstractVariableCode] = []

    @abstractmethod
    def __init__(self, **kwargs: dict[str, Any]):
        pass  # pragma: no cover

    @abstractmethod
    def __str__(self) -> str:
        pass  # pragma: no cover

    @property
    def imports_code(self) -> str:
        res: list[str] = []
        for module, classes in self.imports.items():
            if classes:
                res.append(f"from {module} import {', '.join(sorted(classes))}")
            else:
                res.append(f'import {module}')
        return '\n'.join(res)

    @property
    def variables_code(self) -> str:
        return '\n'.join([str(var) for var in self.variables])

    @property
    def classes_code(self) -> str:
        return '\n'.join([str(_class) for _class in self.classes])

    @property
    def functions_code(self) -> str:
        return '\n'.join([str(func) for func in self.functions])

    @property
    def type_checking_imports_code(self) -> str:
        if not self.type_checking_imports:
            return ''  # pragma: no cover
        imports = '\n'.join(
            [
                f"from {module} import {', '.join(sorted(classes))}"
                for module, classes in self.type_checking_imports.items()
            ]
        )
        return f"""
if TYPE_CHECKING:
{ident_text(imports,1)}
"""


class SimpleModuleCode(AbstractModuleCode):
    @abstractmethod
    def __init__(self, config: NameConfig, app_obj: AppObject | None = None):
        pass  # pragma: no cover

    @abstractmethod
    def __str__(self) -> str:
        pass  # pragma: no cover
