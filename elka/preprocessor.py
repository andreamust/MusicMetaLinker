import spacy

nlp = spacy.load('en_core_web_lg')

if __name__ == '__main__':
    # try spacy entity recognizer
    doc = nlp(u'Rolling Stones and The Beatles are both British rock bands.')
    nlp.add_pipe('entityfishing')
    for ent in doc.ents:
        print((ent.text, ent.label_, ent._.kb_qid, ent._.url_wikidata, ent._.nerd_score))
