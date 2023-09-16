from pathlib import Path


def ident_text(text: str, nr_tabs: int) -> str:
    tab_distance = '    '
    splited_text = text.split(sep='\n')
    result: list[str] = []
    for t in splited_text:
        tabs = ''
        for _ in range(nr_tabs):
            tabs += tab_distance
        if t != '':
            result.append(tabs + t)
    text_res = '\n'.join(result) + '\n'
    return text_res


def get_module_str(current_module: str, dependency: str) -> str:
    main_path = 'app/'
    curent_path = Path(main_path + current_module)
    dep_path = Path(main_path + dependency).parent
    res: list[str] = [Path(dependency).name]
    dots_num = 1
    i = 0
    for i in range(10):
        if curent_path.is_relative_to(dep_path):
            break
        res.append(dep_path.name)
        dep_path = dep_path.parent
    current_parent = curent_path.parent
    if i >= 9:
        raise RuntimeError("Can't parse more then 10 folder deep modules")
    for i in range(10):
        if dep_path.is_relative_to(current_parent):
            break
        dots_num += 1
        current_parent = current_parent.parent
    if i >= 9:
        raise RuntimeError("Can't parse more then 10 folder deep modules")

    rel = dots_num * '.' + '.'.join(res[::-1])
    return rel
