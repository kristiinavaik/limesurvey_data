"""
Viib Limesurvey tekstid Stanzaga sobivasse vormi.
Eesmärk: tunnuste eraldamiseks on vaja, et sisend oleks sobival kujul.
Väljund -> üks tekst per rida -> [faili_id, [[sõne1, sõne1_lemma, sõne1_ POS, sõne_morf], [repeat], ...]]
"""
from pathlib import Path
import stanza
import jsonlines
import torch
torch.set_num_threads(2)
nlp = stanza.Pipeline('et', verbose=False, use_gpu=False)


def analyysi(doc):
    line_lst = []
    txt = nlp(doc)
    sentences = [sent for sent in txt.sentences]

    for sent in sentences:
        sent_words = [w for w in sent.words]
        for w in sent_words:
            token = w.text
            lemma = w.lemma
            pos = w.upos
            if w.feats is None:
                morf = '_'
            else:
                morf = w.feats

            word_info = [token, lemma, pos, morf]

            line_lst.append(word_info)
    return line_lst

def main():
    docs = []
    dir = '../katsed/limesurvey_data/tekstid/'
    paths = [p for p in Path(dir).glob('*.txt')][:1]
    with jsonlines.open('../proov.json', mode='w') as writer:
        for path in paths:
            filename = path.stem
            print(filename)
            with open(path) as fod:
                doc = ' '.join([line for line in fod.readlines()])
                analyys = analyysi(doc)

                # writer.write([filename, analyys])


if __name__ == '__main__':
    main()
    # print('Boo')
