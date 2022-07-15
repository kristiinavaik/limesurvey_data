from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Iterator, Sequence, List
import re

# dataclassi kasutamise näide:
# https://docs.python.org/3/library/dataclasses.html#dataclasses.asdict

lexicon_dir = './lexicons'

# lexicons
core_verbs = [line.strip() for line in open(f"{lexicon_dir}/core_verbs")]




@dataclass
class WordInfo:
    word: str
    lemma: str
    pos_tag: str
    morf_analysis: str


class Text:
    def __init__(self, file_id: str, words_info: Sequence[WordInfo]):
        self.file_id = file_id
        self.words_info = words_info

    @classmethod
    def from_input(cls, input_text: Tuple[str, Tuple[str, str, str, str]]) -> Text:
        file_id, words_analysis = input_text
        return cls(file_id, [WordInfo(*si) for si in words_analysis])

    @property
    def normalize(cls) -> float:
        return cls.get_text_length() + 0.000001

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


    # SÕNALIIGID (va verb, adv)

    def get_nouns(self) -> float:
        return sum(pos == 'NOUN' for pos in self.pos_tags)

    def get_adjectives(self) -> float:
        return sum(pos == 'ADJ' for pos in self.pos_tags)

    def get_propn(self) -> float:
        return sum(pos == 'PROPN' for pos in self.pos_tags)

    # def get_adv(self) -> float:
    #     return sum(pos == 'ADV' for pos in self.pos_tags)

    def get_intj(self) -> float:
        return sum(pos == 'INTJ' for pos in self.pos_tags)

    def get_cconj(self) -> float:
        return sum(pos == 'CCONJ' for pos in self.pos_tags)

    def get_sconj(self) -> float:
        return sum(pos == 'SCONJ' for pos in self.pos_tags)

    def get_adp(self) -> float:
        return sum(pos == 'ADP' for pos in self.pos_tags)

    def get_det(self) -> float:
        return sum(pos == 'DET' for pos in self.pos_tags)

    def get_num(self) -> float:
        return sum(pos == 'NUM' for pos in self.pos_tags)

    def get_punct(self) -> float:
        return sum(pos == 'PUNCT' for pos in self.pos_tags)

    def get_symbols(self) -> float:
        return sum(pos == 'SYM' for pos in self.pos_tags)

    def get_particles(self) -> float:
        return sum(pos == 'PART' for pos in self.pos_tags)

    def get_prons(self) -> float:
        return sum(pos == 'PRON' for pos in self.pos_tags)

    # TEKSTILISED TUNNUSED

    def get_text_length(self) -> int:
        return len(self.words_info)

    def get_TTR(self) -> float:
        """type-token ratio"""
        unique_tokens = set([word_info.word for word_info in self.words_info if word_info.pos_tag != 'PUNCT'])
        return len(unique_tokens)/self.normalize

    # VARIA

    def get_coreference(self) -> float:
        return self.get_prons()/self.get_nouns()

    def get_see_word(self) -> float:
        return sum(lemma == 'see' for lemma in self.lemmas)

    # VERBS

    def get_first_pron(self) -> int:
        ls = [w for w in self.words_info if w.pos_tag in ['AUX', 'VERB'] and re.match(w.morf_analysis, 'Person=1')]
        return len(ls)

    def get_second_pron(self) -> int:
        ls = [w for w in self.words_info if w.pos_tag in ['AUX', 'VERB'] and re.match(w.morf_analysis, 'Person=2')]
        return len(ls)

    def get_third_pron(self) -> int:
        ls = [w for w in self.words_info if w.pos_tag in ['AUX', 'VERB'] and re.match(w.morf_analysis, 'Person=3')]
        return len(ls)

    def get_active_voice(self) -> int:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Voice=Act')])

    def get_passive_voice(self) -> int:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Voice=Pass')])

    def get_core_verbs(self) -> float:
        return len([lemma for lemma in self.lemmas if lemma in core_verbs])

    def get_non_core_verbs(self) -> float:
        return len([pair for pair in zip(self.pos_tags, self.lemmas) if pair[0] == 'VERB' and pair[1] not in core_verbs])

    def get_finite_verbs(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'VerbForm=Fin')])/self.normalize

    def get_infinite_verbs(self) -> float:
        infinite_pattern = re.compile('VerbForm=(Sup|Conv|Part|Inf)')
        matches = [w for w in self.words_info if infinite_pattern.search(w.morf_analysis)]
        return len(matches)/self.normalize

    def get_verbtype_ratio(self) -> float:
        return self.get_finite_verbs()/self.get_infinite_verbs()

    def get_da_infinitive(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'VerbForm=Inf')])

    def get_gerunds(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'VerbForm=Conv')])

    def get_present_tense(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Tense=Pres')])

    def get_past_tense(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Tense=Past')])

    def get_indicative_mood(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Mood=Ind')])

    def get_conditional_mood(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Mood=Cnd')])

    def get_imperative_mood(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Mood=Imp')])

    def get_quotative_mood(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Mood=Qot')])

    # KÄÄNDED

    def get_nominative(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Case=Nom')])

    def get_genitive(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Case=Gen')])

    def get_partitive(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Case=Par')])

    def get_illative(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Case=Ill')])

    def get_inessive(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Case=Ine')])

    def get_elative(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Case=Ela')])

    def get_allative(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Case=All')])

    def get_adessive(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Case=Ade')])

    def get_ablative(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Case=Abl')])

    def get_transitive(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Case=Tra')])

    def get_terminative(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Case=Ter')])

    def get_essive(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Case=Ess')])

    def get_abessive(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Case=Abe')])

    def get_comitative(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Case=Com')])



def main():
    # input_text = [
    #     'faili_id',
    #     [
    #         ['Peetri', 'Peeter', 'sub', 'ahv bahv'],
    #         ['autoga', 'auto', 'NOUN', 'bla bla bla'],
    #         ['sõideti', 'sõitma', 'verb', 'veerib verbe'],
    #         ["meist", "mina", "PRON", "Case=Ela|Number=Plur|Person=3|PronType=Prs|Voice=Act"]
    #     ],
    # ]

    input_text = [
        "www_post_ee.ela_149870",
        [
            ["8.", "8.", "ADJ", "Case=Nom|NumForm=Digit|NumType=Ord|Number=Sing"], ["detsember", "detsember", "NOUN", "Case=Nom|Number=Sing"], ["2011", "2011", "NUM", "Case=Gen|NumForm=Digit|NumType=Card|Number=Sing"], ["Eesti", "Eesti", "PROPN", "Case=Gen|Number=Sing"], ["Posti", "Post", "PROPN", "Case=Gen|Number=Sing"], ["nõukogu", "nõu_kogu", "NOUN", "Case=Nom|Number=Sing"], ["kuulutas", "kuulutama", "VERB", "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act"], ["välja", "välja", "ADV", "_"], ["konkursi", "konkurss", "NOUN", "Case=Gen|Number=Sing"], ["juhatuse", "juhatus", "NOUN", "Case=Gen|Number=Sing"], ["esimehe", "esi_mees", "NOUN", "Case=Gen|Number=Sing"], ["kohale", "kohale", "ADP", "AdpType=Post"], ["Posti-", "Post", "PROPN", "Case=Gen|Hyph=Yes|Number=Sing"], ["ja", "ja", "CCONJ", "_"], ["logistikaettevõtte", "logistika_ette_võte", "NOUN", "Case=Gen|Number=Sing"], ["nõukogu", "nõu_kogu", "NOUN", "Case=Nom|Number=Sing"], ["kuulutas", "kuulutama", "VERB", "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act"], ["välja", "välja", "ADV", "_"], ["konkursi", "konkurss", "NOUN", "Case=Gen|Number=Sing"], ["juhatuse", "juhatus", "NOUN", "Case=Gen|Number=Sing"], ["esimehe", "esi_mees", "NOUN", "Case=Gen|Number=Sing"], ["ametikohale", "ameti_koht", "NOUN", "Case=All|Number=Sing"], [",", ",", "PUNCT", "_"], ["kandidaatide", "kandidaat", "NOUN", "Case=Gen|Number=Plur"], ["avaldusi", "avaldus", "NOUN", "Case=Par|Number=Plur"], ["oodatakse", "ootama", "VERB", "Mood=Ind|Tense=Pres|VerbForm=Fin|Voice=Pass"], ["15.", "15.", "ADJ", "Case=Gen|NumForm=Digit|NumType=Ord|Number=Sing"], ["jaanuarini", "jaanuar", "NOUN", "Case=Ter|Number=Sing"], ["2012", "2012", "NUM", "Case=Nom|NumForm=Digit|NumType=Card|Number=Sing"], ["(", "(", "PUNCT", "_"], ["k.a", "k.a", "ADV", "Abbr=Yes"], [")", ")", "PUNCT", "_"], [".", ".", "PUNCT", "_"], ["Ettevõtte", "ette_võte", "NOUN", "Case=Gen|Number=Sing"], ["nõukogu", "nõu_kogu", "NOUN", "Case=Nom|Number=Sing"], ["soovib", "soovima", "VERB", "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act"], ["Eesti", "Eesti", "PROPN", "Case=Gen|Number=Sing"], ["Posti", "Post", "PROPN", "Case=Gen|Number=Sing"], ["juhatuse", "juhatus", "NOUN", "Case=Gen|Number=Sing"], ["esimehe", "esi_mees", "NOUN", "Case=Gen|Number=Sing"], ["kandidaadilt", "kandidaat", "NOUN", "Case=Abl|Number=Sing"], ["rahvusvahelist", "rahvus_vaheline", "ADJ", "Case=Par|Degree=Pos|Number=Sing"], ["juhtimiskogemust", "juht_imis_kogemus", "NOUN", "Case=Par|Number=Sing"], [".", ".", "PUNCT", "_"], ["Kandidaadil", "kandidaat", "NOUN", "Case=Ade|Number=Sing"], ["peab", "pidama", "AUX", "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act"], ["olema", "olema", "AUX", "Case=Ill|VerbForm=Sup|Voice=Act"], ["vähemalt", "vähemalt", "ADV", "_"], ["kolmeaastane", "kolme_aastane", "ADJ", "Case=Nom|Degree=Pos|Number=Sing"], ["keskmise", "keskmine", "ADJ", "Case=Gen|Degree=Pos|Number=Sing"], ["või", "või", "CCONJ", "_"], ["suurettevõtte", "suur_ette_võte", "NOUN", "Case=Gen|Number=Sing"], ["juhtimiskogemus", "juhtimis_kogemus", "NOUN", "Case=Nom|Number=Sing"], ["ning", "ning", "CCONJ", "_"], ["kasuks", "kasu", "NOUN", "Case=Tra|Number=Sing"], ["tuleb", "tulema", "VERB", "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act"], ["töökogemus", "töö_kogemus", "NOUN", "Case=Nom|Number=Sing"], ["rahvusvahelises", "rahvus_vaheline", "ADJ", "Case=Ine|Degree=Pos|Number=Sing"], ["ettevõttes", "ette_võte", "NOUN", "Case=Ine|Number=Sing"], [".", ".", "PUNCT", "_"], ["Kanditaat", "kanditaat", "NOUN", "Case=Nom|Number=Sing"], ["peab", "pidama", "AUX", "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act"], ["esitama", "esitama", "VERB", "Case=Ill|VerbForm=Sup|Voice=Act"], ["lisaks", "lisa", "NOUN", "Case=Tra|Number=Sing"], ["CV-le", "CV", "PROPN", "Abbr=Yes|Case=All|Number=Sing"], ["nägemuse", "nägemus", "NOUN", "Case=Gen|Number=Sing"], ["Eesti", "Eesti", "PROPN", "Case=Gen|Number=Sing"], ["Posti", "Post", "PROPN", "Case=Gen|Number=Sing"], ["lähiaastate", "lähi_aasta", "NOUN", "Case=Gen|Number=Plur"], ["strateegilistest", "strateegiline", "ADJ", "Case=Ela|Degree=Pos|Number=Plur"], ["suundadest", "suund", "NOUN", "Case=Ela|Number=Plur"], [".", ".", "PUNCT", "_"], ["Eesti", "Eesti", "PROPN", "Case=Gen|Number=Sing"], ["Posti", "Post", "PROPN", "Case=Gen|Number=Sing"], ["nõukogu", "nõu_kogu", "NOUN", "Case=Nom|Number=Sing"], ["rahuldas", "rahuldama", "VERB", "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act"], ["novembri", "november", "NOUN", "Case=Gen|Number=Sing"], ["lõpus", "lõpp", "NOUN", "Case=Ine|Number=Sing"], ["juhatuse", "juhatus", "NOUN", "Case=Gen|Number=Sing"], ["esimees", "esi_mees", "NOUN", "Case=Nom|Number=Sing"], ["Ahti", "Ahti", "PROPN", "Case=Nom|Number=Sing"], ["Kallaste", "Kallaste", "PROPN", "Case=Gen|Number=Sing"], ["lahkumisavalduse", "lahkumis_avaldus", "NOUN", "Case=Gen|Number=Sing"], [".", ".", "PUNCT", "_"], ["Kallaste", "Kallaste", "PROPN", "Case=Nom|Number=Sing"], ["lahkub", "lahkuma", "VERB", "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act"], ["ettevõttest", "ette_võte", "NOUN", "Case=Ela|Number=Sing"], ["alates", "alates", "ADP", "AdpType=Prep"], ["1.", "1.", "ADJ", "Case=Ela|NumForm=Digit|NumType=Ord|Number=Sing"], ["märtsist", "märts", "NOUN", "Case=Ela|Number=Sing"], ["2012", "2012", "NUM", "NumForm=Digit|NumType=Card"], ["ning", "ning", "CCONJ", "_"], ["asub", "asuma", "VERB", "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act"], ["tööle", "töö", "NOUN", "Case=All|Number=Sing"], ["oma", "oma", "PRON", "Case=Gen|Number=Sing|Poss=Yes|PronType=Prs"], ["perekonnale", "perekond", "NOUN", "Case=All|Number=Sing"], ["kuuluvas", "kuuluv", "ADJ", "Case=Ine|Degree=Pos|Number=Sing|Tense=Pres|VerbForm=Part|Voice=Act"], ["meditsiinifirmas", "meditsiini_firma", "NOUN", "Case=Ine|Number=Sing"], [".", ".", "PUNCT", "_"]
        ]
    ]


    # faili_id, sõna_infod = sisend
    # text = Text(faili_id, [SõnaInfo(*si) for si in sõna_infod])

    text = Text.from_input(input_text)
    # print('Sõnainfod on:')
    # for sona_info in text.words_info:
    #     print('\t', sona_info)
    print(
        f'Teksti {text.file_id}\n'
        f'seal on {text.get_nouns()} nimisõna, normaliseeritud nimisõnade hulk {text.get_nouns()/text.normalize}, '
        f'teksti pikkus on {text.get_text_length()}, '
        f'ttr on {text.get_TTR()}\n'
        f'core verbs: {text.get_core_verbs()}, non-core verbs: {text.get_non_core_verbs()}\n'
        f'finite verbs: {text.get_finite_verbs()}\n'
        f'infinite: {text.get_infinite_verbs()}\n'
        f'ratio {text.get_verbtype_ratio()}\n'
        f'{text.get_third_pron()}'

    )


if __name__ == '__main__':
    main()

