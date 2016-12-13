import mulli


def save_paste(id, content, valid=30, lexer=None):
    entry = {'content': content, 'lexer': lexer}
    mulli.add_entry(id, entry, valid)


def remove_paste(id):
    pastes = mulli.load_database()
    del pastes[id]
    mulli.save_database(pastes)
