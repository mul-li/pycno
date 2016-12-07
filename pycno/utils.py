import functools

import mulli


load_pastes = functools.partial(mulli.load_database, filename='pycno.pickle')
save_pastes = functools.partial(mulli.save_database, filename='pycno.pickle')


def create_id(content):
    return mulli.create_id(content, load_pastes())


def save_paste(id, content, valid=30, lexer=None):
    pastes = load_pastes()
    entry = {'content': content, 'lexer': lexer}
    save_pastes(mulli.add_entry(id, entry, valid, pastes))


def remove_paste(id):
    pastes = load_pastes()
    del pastes[id]
    save_pastes(pastes)


def load_paste(paste_id):
    paste = mulli.load_entry(paste_id, load_pastes())
    return paste['content']


def load_lexer(paste_id):
    paste = mulli.load_entry(paste_id, load_pastes())
    return paste['lexer']
