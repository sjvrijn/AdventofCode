# coding: utf-8


def a(declaration_forms):
    group_forms = []
    form = set()
    for f in declaration_forms:
        if not f:
            group_forms.append(form)
            form = set()
        else:
            form |= f
    group_forms.append(form)
    return sum(len(gf) for gf in group_forms)


def b(declaration_forms):
    group_forms = []
    declaration_forms_iter = iter(declaration_forms)
    form = next(declaration_forms_iter)
    for f in declaration_forms_iter:
        if not f:
            group_forms.append(form)
            form = next(declaration_forms_iter)
        else:
            form &= f
    group_forms.append(form)
    return sum(len(gf) for gf in group_forms)


if __name__ == '__main__':
    with open('input06.txt') as f:
        declaration_forms = [set(line.strip()) for line in f]

    print(a(declaration_forms))
    print(b(declaration_forms))
