import spacy

nlp = spacy.load('en_core_web_lg')

if __name__ == '__main__':
    # try spacy entity recognizer
    nlp.add_pipe("entityLinker", last=True)
    doc = nlp(u'Rolling Stones')

    # returns all entities in the whole document
    all_linked_entities = doc._.linkedEntities
    # iterates over sentences and prints linked entities
    for sent in doc.sents:
        sent._.linkedEntities.pretty_print()
