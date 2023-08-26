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
