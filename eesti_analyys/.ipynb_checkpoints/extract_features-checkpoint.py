from __future__ import annotations

import csv
import re
from collections import Counter
import collections
from dataclasses import dataclass
from typing import Tuple, Iterator, Sequence

import jsonlines

# dataclassi kasutamise näide:
# https://docs.python.org/3/library/dataclasses.html#dataclasses.asdict

lexicon_dir = './lexicons'

# lexicons
core_verbs = [line.strip() for line in open(f"{lexicon_dir}/core_verbs")]
yneemid = [line.strip() for line in open(f"{lexicon_dir}/yneemid")] # võtsin siit: https://www.cl.ut.ee/suuline/Transk.php (saaks alati täiendada)
emoticons = [line.strip() for line in open(f"{lexicon_dir}/wikipedia_emoticons_list.txt")]

constant = 1

@dataclass
class WordInfo:
    word: str
    lemma: str
    pos_tag: str
    morf_analysis: str
    dep: str


class Text:
    def __init__(self, file_id: str, avg_sent_len: float, words_info: Sequence[WordInfo]):
        self.file_id = file_id
        self.avg_sent_len = avg_sent_len
        self.words_info = words_info

    @classmethod
    def from_input(cls, input_text: Tuple[str, int, Tuple[str, str, str, str, str]]) -> Text:
        file_id, sent, words_analysis = input_text
        return cls(file_id, sent, [WordInfo(*si) for si in words_analysis])

    @property
    def normalize(cls) -> float:
        return cls.get_text_length()

    @property
    def raw_text(self) -> Iterator[str]:
        return (word_info.word for word_info in self.words_info)

    @property
    def lemmas(self) -> Iterator[str]:
        return (word_info.lemma for word_info in self.words_info)

    @property
    def pos_tags(self) -> Iterator[str]:
        return (word_info.pos_tag for word_info in self.words_info)

    @property
    def morf_analysis(self) -> Iterator[str]:
        return (word_info.morf_analysis for word_info in self.words_info)

    def get_raw_text(self) -> str:
        return ' '.join(self.raw_text)

    def get_text_length(self) -> int:
        return len(self.words_info)

    # SÕNALIIGID (va verb, adv)

    def get_nouns(self) -> float:
        return sum(pos == 'NOUN' for pos in self.pos_tags) / self.get_text_length()

    def get_adjectives(self) -> float:
        return sum(pos == 'ADJ' for pos in self.pos_tags) / self.get_text_length()

    def get_propn(self) -> float:
        return sum(pos == 'PROPN' for pos in self.pos_tags) / self.get_text_length()

    def get_adv(self) -> float:
        return sum(pos == 'ADV' for pos in self.pos_tags) / self.get_text_length()

    def get_intj(self) -> float:
        return sum(pos == 'INTJ' for pos in self.pos_tags) / self.get_text_length()

    def get_cconj(self) -> float:
        return sum(pos == 'CCONJ' for pos in self.pos_tags) / self.get_text_length()

    def get_sconj(self) -> float:
        return (sum(pos == 'SCONJ' for pos in self.pos_tags) / self.get_text_length()

    def get_adp(self) -> float:
        return sum(pos == 'ADP' for pos in self.pos_tags) / self.get_text_length()

    def get_det(self) -> float:
        return sum(pos == 'DET' for pos in self.pos_tags) / self.get_text_length()

    def get_num(self) -> float:
        return (sum(pos == 'NUM' for pos in self.pos_tags) / self.get_text_length()

    def get_punct(self) -> float:
        return sum(pos == 'PUNCT' for pos in self.pos_tags) / self.get_text_length()

    def get_symbols(self) -> float:
        return sum(pos == 'SYM' for pos in self.pos_tags) / self.get_text_length()

    # def get_particles(self) -> float:
    #     return (len([pos for pos in self.pos_tags if pos == 'PART']) + constant) / self.get_text_length()

    def get_prons(self) -> float:
        return sum(pos == 'PRON' for pos in self.pos_tags) / self.get_text_length()

    def get_abbriviations(self) -> float:
        return len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Abbr=Yes')]) / self.get_text_length()

    # TEKSTILISED TUNNUSED

    # + constant) / self.get_text_length()

    def get_TTR(self) -> float:
        """type-token ratio, seda EI peaks normaliseerima"""
        words_count = len([w for w in self.words_info])
        unique_tokens = set([word_info.word for word_info in self.words_info if word_info.pos_tag != 'PUNCT'])
        return len(unique_tokens) / words_count

    def get_average_word_length(self) -> float:
        """seda EI peaks normaliseerima"""
        words_count = len([w for w in self.words_info])
        average_len = sum(len(word_info.word) for word_info in self.words_info) / words_count
        return average_len

    def get_hapax_legomena(self) -> float:
        counts = Counter([w.lemma for w in self.words_info])
        hapaxes = [word for word in counts if counts[word] == 1]
        return (float(len(hapaxes) + constant)) / self.get_text_length()

    # VARIA

    def get_coreference(self) -> float:
        return self.get_prons() / self.get_nouns()

    def get_see_as_pronoun(self) -> float:
        matches = [w for w in self.words_info if w.lemma == 'see' and w.pos_tag == 'PRON']
        return len(matches) / self.get_text_length()

    def get_see_as_determinant(self):
        matches = [w for w in self.words_info if w.lemma == 'see' and w.pos_tag == 'DET']
        return len(matches) / self.get_text_length()

    def get_first_pron(self) -> float:
        ls = [w for w in self.words_info if w.pos_tag == 'PRON' and re.match(w.morf_analysis, 'Person=1')]
        return len(ls) / self.get_text_length()

    def get_second_pron(self) -> float:
        ls = [w for w in self.words_info if w.pos_tag == 'PRON' and re.match(w.morf_analysis, 'Person=2')]
        return len(ls) / self.get_text_length()

    def get_third_pron(self) -> float:
        ls = [w for w in self.words_info if w.pos_tag == 'PRON' and re.match(w.morf_analysis, 'Person=3')]
        return len(ls) / self.get_text_length()

    # VERBS

    def get_active_voice(self) -> float:
        return len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Voice=Act')]) / self.get_text_length()

    def get_passive_voice(self) -> float:
        return len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Voice=Pass')]) / self.get_text_length()

    def get_first_person_verbs(self) -> float:
        ls = [w for w in self.words_info if w.pos_tag in ['AUX', 'VERB'] and re.match(w.morf_analysis, 'Person=1')]
        return len(ls) / self.get_text_length()

    def get_second_person_verbs(self) -> float:
        ls = [w for w in self.words_info if w.pos_tag in ['AUX', 'VERB'] and re.match(w.morf_analysis, 'Person=2')]
        return len(ls) / self.get_text_length()

    def get_third_person_verbs(self) -> float:
        ls = [w for w in self.words_info if w.pos_tag in ['AUX', 'VERB'] and re.match(w.morf_analysis, 'Person=3')]
        return len(ls) / self.get_text_length()

    def get_core_verbs(self) -> float:
        return len([lemma for lemma in self.lemmas if lemma in core_verbs]) / self.get_text_length()

    # läheb vaja ainult get_verbtype_ratio arvutamises
    def get_finite_verbs(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'VerbForm=Fin')])

    # läheb vaja ainult get_verbtype_ratio arvutamises
    def get_infinite_verbs(self) -> float:
        infinite_pattern = re.compile('VerbForm=(Sup|Conv|Part|Inf)')
        matches = [w for w in self.words_info if infinite_pattern.search(w.morf_analysis)]
        return len(matches)

    def get_verbtype_ratio(self) -> float:
        """ EI PEA NORMALISEERIMA"""
        return self.get_finite_verbs() / self.get_infinite_verbs()

    def get_da_infinitive(self) -> float:
        return len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'VerbForm=Inf')]) / self.get_text_length()

    def get_gerunds(self) -> float:
        return len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'VerbForm=Conv')]) / self.get_text_length()

    def get_supine(self) -> float:
        return len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'VerbForm=Sup')]) / self.get_text_length()

    def get_verb_particles(self) -> float:
        return len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'VerbForm=Part')]) / self.get_text_length()

    def get_present_tense(self) -> float:
        return len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Tense=Pres')]) / self.get_text_length()

    def get_past_tense(self) -> float:
        return len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Tense=Past')]) / self.get_text_length()

    def get_indicative_mood(self) -> float:
        return len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Mood=Ind')]) / self.get_text_length()

    def get_conditional_mood(self) -> float:
        return len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Mood=Cnd')]) / self.get_text_length()

    def get_imperative_mood(self) -> float:
        return len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Mood=Imp')]) / self.get_text_length()

    def get_quotative_mood(self) -> float:
        return len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Mood=Qot')]) / self.get_text_length()

    def get_negative_polarity(self) -> float:
        return len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Polarity=Neg')]) / self.get_text_length()

    # KÄÄNDED

    def get_nominative(self) -> float:
        return len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Case=Nom')]) / self.get_text_length()

    def get_genitive(self) -> float:
        return len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Case=Gen')]) / self.get_text_length()

    def get_partitive(self) -> float:
        return len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Case=Par')]) / self.get_text_length()

    def get_illative(self) -> float:
        return len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Case=Ill')]) / self.get_text_length()

    def get_inessive(self) -> float:
        return len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Case=Ine')]) / self.get_text_length()

    def get_elative(self) -> float:
        return (len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Case=Ela')]) + constant) / self.get_text_length()

    def get_allative(self) -> float:
        return (len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Case=All')]) + constant) / self.get_text_length()

    def get_adessive(self) -> float:
        return (len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Case=Ade')]) + constant) / self.get_text_length()

    def get_ablative(self) -> float:
        return (len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Case=Abl')]) + constant) / self.get_text_length()

    def get_transitive(self) -> float:
        return (len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Case=Tra')]) + constant) / self.get_text_length()

    def get_terminative(self) -> float:
        return (len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Case=Ter')]) + constant) / self.get_text_length()

    def get_essive(self) -> float:
        return (len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Case=Ess')]) + constant) / self.get_text_length()

    def get_abessive(self) -> float:
        return (len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Case=Abe')]) + constant) / self.get_text_length()

    def get_comitative(self) -> float:
        return (len([w for w in self.words_info if
                     re.match(w.morf_analysis, 'Case=Com')]) + constant) / self.get_text_length()

    # SÜNTAKS (pärinevad siit: https://github.com/EstSyntax/EstUD/blob/master/EestiUDdokumentatsioon.pdf)

    def get_nsubj(self) -> float:
        return (len([w for w in self.words_info if re.match(w.dep, 'nsubj$')]) + constant) / self.get_text_length()

    def get_nsubj_cop(self) -> float:
        cop_patt = re.compile('nsubj:cop$')
        return (len([w for w in self.words_info if cop_patt.search(w.dep)]) + constant) / self.get_text_length()

    def get_modals(self) -> float:
        return (len([w for w in self.words_info if w.dep == 'aux']) + constant) / self.get_text_length()

    def get_relative_clause_modifier(self) -> float:
        cop_patt = re.compile('acl:relcl$')
        return (len([w for w in self.words_info if cop_patt.search(w.dep)]) + constant) / self.get_text_length()

    def get_csubj(self) -> float:
        return (len([w for w in self.words_info if re.match(w.dep, 'csubj$')]) + constant) / self.get_text_length()

    def get_csubj_cop(self) -> float:
        csub_cop_patt = re.compile('csubj:cop$')
        return (len([w for w in self.words_info if csub_cop_patt.search(w.dep)]) + constant) / self.get_text_length()

    def get_obj(self) -> float:
        return (len([w for w in self.words_info if re.match(w.dep, 'obj$')]) + constant) / self.get_text_length()

    def get_xcomp(self) -> float:
        return (len([w for w in self.words_info if re.match(w.dep, 'xcomp')]) + constant) / self.get_text_length()

    def get_ccomp(self) -> float:
        return (len([w for w in self.words_info if re.match(w.dep, 'ccomp')]) + constant) / self.get_text_length()

    def get_obl(self) -> float:
        return (len([w for w in self.words_info if re.match(w.dep, 'obl')]) + constant) / self.get_text_length()

    def get_nmod(self) -> float:
        return (len([w for w in self.words_info if re.match(w.dep, 'nmod')]) + constant) / self.get_text_length()

    def get_appos(self) -> float:
        return (len([w for w in self.words_info if re.match(w.dep, 'appos')]) + constant) / self.get_text_length()

    def get_nummod(self) -> float:
        return (len([w for w in self.words_info if re.match(w.dep, 'nummod')]) + constant) / self.get_text_length()

    def get_amod(self) -> float:
        return (len([w for w in self.words_info if re.match(w.dep, 'amod')]) + constant) / self.get_text_length()

    def get_advcl(self) -> float:
        return (len([w for w in self.words_info if re.match(w.dep, 'advcl')]) + constant) / self.get_text_length()

    def get_vocative(self) -> float:
        return (len([w for w in self.words_info if re.match(w.dep, 'vocative')]) + constant) / self.get_text_length()

    def get_cop(self) -> float:
        return (len([w for w in self.words_info if re.match(w.dep, 'cop')]) + constant) / self.get_text_length()

    def get_discourse(self) -> float:
        # print(len([w for w in self.words_info if re.match(w.dep, 'discourse')]))
        return (len([w for w in self.words_info if re.match(w.dep, 'discourse')]) + constant) / self.get_text_length()

    def get_conj(self) -> float:
        return (len([w for w in self.words_info if re.match(w.dep, 'conj')]) + constant) / self.get_text_length()

    def get_cc(self) -> float:
        return (len([w for w in self.words_info if re.match(w.dep, 'cc')]) + constant) / self.get_text_length()

    # lexicons

    def get_yneemid(self) -> float:
        return (len([w for w in self.raw_text if w in yneemid]) + constant) / self.get_text_length()

    def get_emoticons(self) -> float:
        return (len([word for word in self.raw_text if word in emoticons]) + constant) / self.get_text_length()

    def get_feature_mapping(self):
        return {
            'file_id': self.file_id,
            'noun': self.get_nouns(),
            'adj': self.get_adjectives(),
            'propn': self.get_propn(),
            'adv': self.get_adv(),
            'intj': self.get_intj(),
            'cconj': self.get_cconj(),
            'sconj': self.get_sconj(),
            'adp': self.get_adp(),
            'det': self.get_det(),
            'num': self.get_num(),
            'punct': self.get_punct(),
            'symbol': self.get_symbols(),
            # 'particle': self.get_particles(),
            'discourse': self.get_discourse(),
            'pron': self.get_prons(),
            'abbr': self.get_abbriviations(),
            # 'txt_len': # text.get_text_length
            'TTR': self.get_TTR(),
            'avg_word_len': self.get_average_word_length(),
            'avr_sent_len': self.avg_sent_len,
            'hapax_legomena': self.get_hapax_legomena(),
            'coref': self.get_coreference(),
            'see_pron': self.get_see_as_pronoun(),
            'see_det': self.get_see_as_determinant(),
            '1st_pron': self.get_first_pron(),
            '2nd_pron': self.get_second_pron(),
            '3rd_pron': self.get_third_pron(),
            'active_voice': self.get_active_voice(),
            'passive_voice': self.get_passive_voice(),
            '1st_prs_verb': self.get_first_person_verbs(),
            '2nd_prs_verb': self.get_second_person_verbs(),
            '3rd_prs_verb': self.get_third_person_verbs(),
            'core_verb': self.get_core_verbs(),
            'verbtype_ratio': self.get_verbtype_ratio(),
            'da_inf': self.get_da_infinitive(),
            'gerund': self.get_gerunds(),
            'supine': self.get_supine(),
            'verb_particle': self.get_verb_particles(),
            'pres_tense': self.get_present_tense(),
            'past_tense': self.get_past_tense(),
            'ind_mood': self.get_indicative_mood(),
            'cond_mood': self.get_conditional_mood(),
            'imp_mood': self.get_imperative_mood(),
            'quot_mood': self.get_quotative_mood(),
            'neg_polarity': self.get_negative_polarity(),
            'nom_case': self.get_nominative(),
            'gen_case': self.get_genitive(),
            'part_case': self.get_partitive(),
            'ill_case': self.get_illative(),
            'ine_case': self.get_inessive(),
            'ela_case': self.get_elative(),
            'alla_case': self.get_allative(),
            'ade_case': self.get_adessive(),
            'abl_case': self.get_ablative(),
            'tra_case': self.get_transitive(),
            'ter_case': self.get_terminative(),
            'ess_case': self.get_essive(),
            'abe_case': self.get_abessive(),
            'com_case': self.get_comitative(),
            'nsubj': self.get_nsubj(),
            'nsubj_cop': self.get_nsubj_cop(),
            'modal': self.get_modals(),
            'acl:relc': self.get_relative_clause_modifier(),
            'csubj': self.get_csubj(),
            'csubj_cop': self.get_csubj_cop(),
            'obj': self.get_obj(),
            'ccomp': self.get_ccomp(),
            'xcomp': self.get_xcomp(),
            'obl': self.get_obl(),
            'nmod': self.get_nmod(),
            'appos': self.get_appos(),
            'nummod': self.get_nummod(),
            'amod': self.get_amod(),
            'advcl': self.get_advcl(),
            'voc': self.get_vocative(),
            'cop': self.get_cop(),
            'conj': self.get_conj(),
            'cc': self.get_cc(),
            'yneemid': self.get_yneemid(),
            'emoticons': self.get_emoticons(),
        }


def main():
    f = 'limesurvey_tekstid_morfiga_vol2.json'
    texts = []
    with jsonlines.open(f) as reader:
        for obj in reader:
            texts.append(obj)

    # for t in texts:
    #     text = Text.from_input(t)
    #     d = {}
    #     d[text.file_id] = text.get_discourse()
    #
    #     for k,v in sorted(d.items()):
    #         print(f'{k} === {v}')

    feature_names = (
    'file_id', 'noun', 'adj', 'propn', 'adv', 'intj', 'cconj', 'sconj', 'adp', 'det', 'num', 'punct', 'symbol',
    'pron', 'abbr', 'TTR', 'avg_word_len', 'avr_sent_len', 'hapax_legomena', 'coref', 'see_pron', 'see_det',
    '1st_pron', '2nd_pron', '3rd_pron', 'active_voice', 'passive_voice', '1st_prs_verb', '2nd_prs_verb', '3rd_prs_verb',
    'core_verb', 'verbtype_ratio', 'da_inf', 'gerund', 'supine', 'verb_particle', 'discourse' , 'pres_tense', 'past_tense',
    'ind_mood', 'cond_mood', 'imp_mood', 'quot_mood', 'neg_polarity', 'nom_case', 'gen_case', 'part_case', 'ill_case',
    'ine_case', 'ela_case', 'alla_case', 'ade_case', 'abl_case', 'tra_case', 'ter_case', 'ess_case', 'abe_case',
    'com_case', 'nsubj', 'nsubj_cop', 'modal', 'acl:relc', 'csubj', 'csubj_cop', 'obj', 'ccomp', 'xcomp', 'obl', 'nmod',
    'appos', 'nummod', 'amod', 'advcl', 'voc', 'cop', 'conj', 'cc', 'yneemid', 'emoticons')


    with open('limesurvey_feature_results2.csv', 'w') as csvfile:
        w = csv.DictWriter(csvfile, feature_names, delimiter=';')
        w.writeheader()

        for t in texts:
            text = Text.from_input(t)
            feature_mapping = text.get_feature_mapping()

            w.writerow(feature_mapping)


if __name__ == '__main__':
    main()
