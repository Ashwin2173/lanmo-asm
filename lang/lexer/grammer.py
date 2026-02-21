TOKEN_GRAMMER = r"""
(?P<COMMENT>//[^\n]*)                                     # single-line comment
| (?P<K_PUSH>PUSH)                                        # push keyword
| (?P<K_POP>POP)                                          # pop keyword
| (?P<K_ADD>ADD)                                          # add keyword
| (?P<K_PEEK>PEEK)                                        # peek keyword
| (?P<K_HALT>HALT)                                        # halt keyword
| (?P<K_EOF>EOF)                                          # eof keyword
| (?P<IDENTIFIER>[A-Za-z_]\w*)                            # identifiers and keywords
| (?P<FLOAT>\d+\.\d+)                                     # float numbers
| (?P<INTEGER>\d+)                                        # integer numbers
| (?P<STRING>"(?:\\.|[^"\\])*")                           # double-quoted strings with escape support
| (?P<OPERATOR>\+=|-=|\*=|/=|%=|==|<=|>=|!=|&&|\|\||=|\+|\-|\*|\/|%|<|>|\(|\)|\{|\}|;|,)  # operators and punctuation
| (?P<DOT_OPERATOR>\.)                                    # dot operator (for object properties/methods)
| (?P<NEWLINE>\n)                                         # new line
"""