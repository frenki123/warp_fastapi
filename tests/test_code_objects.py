import pytest

from warp_fastapi.code.code_objects.base import SimpleClassCode, SimpleDecoratorCode, SimpleFunctionCode, SimpleVariable
from warp_fastapi.code.utils import get_module_str, ident_text


def test_ident_text():
    t1 = """some text


other text
    text"""
    t2 = """        some text
        other text
            text
"""
    t_ident = ident_text(t1, 2)
    print(t_ident)
    print(t2)
    assert t_ident == t2


def test_get_module_str():
    cm = 'm1/m2/m3'
    dm = 'm1/m2/m'
    assert get_module_str(cm, dm) == '.m'
    cm = 'm1/m2/m3/m4/m5'
    dm = 'x/y'
    assert get_module_str(cm, dm) == '.....x.y'
    cm = 'm1/m2/m3/m4/m5/m6/m7/m8/m9/m10'
    dm = 'x'
    with pytest.raises(RuntimeError) as e:
        get_module_str(cm, dm)
    cm = 'm1/m2/m3/m4/m5/m6/m7/m8/m9/m10/m11/m12'
    dm = 'x'
    with pytest.raises(RuntimeError) as e:
        get_module_str(cm, dm)
    assert "Can't parse more then 10 folder deep modules" in str(e)
    cm = 'x'
    dm = 'm1/m2/m3/m4/m5/m6/m7/m8/m9/m10/m11/m12'
    with pytest.raises(RuntimeError) as e:
        get_module_str(cm, dm)
    assert "Can't parse more then 10 folder deep modules" in str(e)


def test_variable():
    v = SimpleVariable('test', 'type', 'value')
    assert str(v) == 'test: type = value'
    v.add_optional()
    assert str(v) == 'test: type | None = value'
    v2 = SimpleVariable('test', 'type | None = value')
    assert v == v2
    v3 = SimpleVariable('test')
    with pytest.raises(ValueError) as e:
        v3.add_optional()
    assert str(e.value) == "Attribute doesn't have a type!"
    assert v3 != 1
    assert str(v3) == 'test'


def test_decorator(variables: list[SimpleVariable]):
    d1 = SimpleDecoratorCode('decorator', list(variables))
    assert str(d1) == '@decorator(num: int = 1, text: str = text)'
    d2 = SimpleDecoratorCode('dec', is_function=True)
    assert str(d2) == '@dec()'
    d3 = SimpleDecoratorCode('dec')
    assert str(d3) == '@dec'


def test_functions(variables: list[SimpleVariable], decorators: list[SimpleDecoratorCode]):
    f1 = SimpleFunctionCode('test', 'return 1')
    assert (
        str(f1)
        == """def test():
    return 1"""
    )
    f2 = SimpleFunctionCode('test', 'return 1', list(variables), 'str', list(decorators))
    assert (
        str(f2)
        == """@dec1()
@dec2
def test(num: int = 1, text: str = text) -> str:
    return 1"""
    )


def test_classes(functions: list[SimpleFunctionCode], variables: list[SimpleVariable]):
    c1 = SimpleClassCode('MyClass', 'BaseModel')
    print(c1)
    assert (
        str(c1)
        == """class MyClass(BaseModel):
    pass"""
    )
    c2 = SimpleClassCode('MyClass', attributes=list(variables), methods=list(functions))
    print(c2)
    assert (
        str(c2)
        == """class MyClass:

    num: int = 1
    text: str = text

    def get_num():
        return 1
    def get_a():
        return a"""
    )
