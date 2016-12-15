import mulli


def save_paste(id, content, valid=30, lexer=None):
    entry = {'content': content, 'lexer': lexer}
    mulli.add_entry(id, entry, valid)
