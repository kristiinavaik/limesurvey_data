from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Iterator, Sequence, List
import re
from collections import Counter

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
    dep: str


class Text:
    def __init__(self, file_id: str, sents: int, words_info: Sequence[WordInfo]):
        self.file_id = file_id
        self.sent_number = sents
        self.words_info = words_info

    @classmethod
    def from_input(cls, input_text: Tuple[str, int, Tuple[str, str, str, str, str]]) -> Text:
        file_id, sent, words_analysis = input_text
        return cls(file_id, sent, [WordInfo(*si) for si in words_analysis])

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

    def get_adv(self) -> float:
        return sum(pos == 'ADV' for pos in self.pos_tags)

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

    def get_abbriviations(self) -> int:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Abbr=Yes')])

    # TEKSTILISED TUNNUSED

    def get_text_length(self) -> int:
        return len(self.words_info)

    def get_TTR(self) -> float:
        """type-token ratio"""
        unique_tokens = set([word_info.word for word_info in self.words_info if word_info.pos_tag != 'PUNCT'])
        return len(unique_tokens)/self.normalize

    def get_average_word_length(self) -> float:
        words_count = len([w for w in self.words_info])
        average = sum(len(word_info.word) for word_info in self.words_info)/words_count
        return average

    def get_hapax_legomena(self) -> int:
        counts = Counter([w.lemma for w in self.words_info])
        hapaxes = [word for word in counts if counts[word] == 1]
        return len(hapaxes)

    # VARIA

    def get_coreference(self) -> float:
        return self.get_prons()/self.get_nouns()

    def get_see_word(self) -> float:
        return sum(lemma == 'see' for lemma in self.lemmas)

    def get_first_pron(self) -> int:
        ls = [w for w in self.words_info if w.pos_tag == 'PRON' and re.match(w.morf_analysis, 'Person=1')]
        return len(ls)

    def get_second_pron(self) -> int:
        ls = [w for w in self.words_info if w.pos_tag == 'PRON' and re.match(w.morf_analysis, 'Person=2')]
        return len(ls)

    def get_third_pron(self) -> int:
        ls = [w for w in self.words_info if w.pos_tag == 'PRON' and re.match(w.morf_analysis, 'Person=3')]
        return len(ls)

    # VERBS

    def get_active_voice(self) -> int:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Voice=Act')])

    def get_passive_voice(self) -> int:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Voice=Pass')])

    def get_first_person_verbs(self) -> int:
        ls = [w for w in self.words_info if w.pos_tag in ['AUX', 'VERB'] and re.match(w.morf_analysis, 'Person=1')]
        return len(ls)

    def get_second_person_verbs(self) -> int:
        ls = [w for w in self.words_info if w.pos_tag in ['AUX', 'VERB'] and re.match(w.morf_analysis, 'Person=2')]
        return len(ls)

    def get_third_person_verbs(self) -> int:
        ls = [w for w in self.words_info if w.pos_tag in ['AUX', 'VERB'] and re.match(w.morf_analysis, 'Person=3')]
        return len(ls)

    def get_core_verbs(self) -> float:
        return len([lemma for lemma in self.lemmas if lemma in core_verbs])

    def get_non_core_verbs(self) -> float:
        return len([pair for pair in zip(self.pos_tags, self.lemmas) if pair[0] == 'VERB' and pair[1] not in core_verbs])

    def get_finite_verbs(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'VerbForm=Fin')])

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

    def get_supine(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'VerbForm=Sup')])

    def get_verb_particles(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'VerbForm=Part')])

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

    def get_negative_polarity(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Polarity=Neg')])

    def get_positive_polarity(self) -> float:
        return len([w for w in self.words_info if re.match(w.morf_analysis, 'Connegative=Yes')])

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

    # SÜNTAKS (pärinevad siit: https://github.com/EstSyntax/EstUD/blob/master/EestiUDdokumentatsioon.pdf)

    def get_nsubj(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'nsubj$')])

    def get_nsubj_cop(self) -> float:
        cop_patt = re.compile('nsubj:cop$')
        return len([w for w in self.words_info if cop_patt.search(w.dep)])

    def get_modals(self) -> int:
        return len([w for w in self.words_info if w.dep == 'aux'])

    def get_relative_clause_modifier(self) -> float:
        cop_patt = re.compile('acl:relcl$')
        return len([w for w in self.words_info if cop_patt.search(w.dep)])

    def get_csubj(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'csubj$')])

    def get_csubj_cop(self) -> float:
        csub_cop_patt = re.compile('csubj:cop$')
        return len([w for w in self.words_info if csub_cop_patt.search(w.dep)])

    def get_obj(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'obj$')])

    def get_xcomp(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'xcomp')])

    def get_ccomp(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'ccomp')])

    def get_obl(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'obl')])

    def get_nmod(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'nmod')])

    def get_appos(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'appos')])

    def get_nummod(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'nummod')])

    def get_amod(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'amod')])

    def get_advcl(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'advcl')])

    def get_vocative(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'vocative')])

    def get_cop(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'cop')])

    def get_mark(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'mark')])

    def get_discourse(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'discourse')])

    def get_parataxis(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'parataxis')])

    def get_list(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'list')])

    def get_conj(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'conj')])

    def get_cc(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'cc')])

    def get_dep(self) -> float:
        return len([w for w in self.words_info if re.match(w.dep, 'dep')])


def main():
    input_text = [
        "www_le_ee.ela_240831", 14,
        [
            ["Eile", "eile", "ADV", "_", "advmod"], ["öösel", "öösel", "ADV", "_", "advmod"],
            ["hävis", "hävima", "VERB", "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act", "root"],
            ["suur", "suur", "ADJ", "Case=Nom|Degree=Pos|Number=Sing", "amod"],
            ["osa", "osa", "NOUN", "Case=Nom|Number=Sing", "nsubj"],
            ["Tokoi", "Tokoi", "PROPN", "Case=Gen|Number=Sing", "nmod"],
            ["pansionaadi", "pansionaat", "NOUN", "Case=Gen|Number=Sing", "nmod"],
            ["sisemusest", "sisemus", "NOUN", "Case=Ela|Number=Sing", "nmod"],
            [",", ",", "PUNCT", "_", "punct"],
            ["külvatud", "külva=tud", "VERB", "Tense=Past|VerbForm=Part|Voice=Pass", "acl:relcl"],
            ["ajaloolises", "aja_looline", "ADJ", "Case=Ine|Degree=Pos|Number=Sing", "amod"],
            ["majas", "maja", "NOUN", "Case=Ine|Number=Sing", "conj"],
            ["Suur–Lossi", "Suur–Loss", "PROPN", "Case=Gen|Number=Sing", "nmod"],
            ["tänaval", "tänav", "NOUN", "Case=Ade|Number=Sing", "nmod"],
            ["põlengu", "põleng", "NOUN", "Case=Gen|Number=Sing", "obl"],
            ["ajal", "ajal", "ADP", "AdpType=Post", "case"],
            ["inimesi", "inimene", "NOUN", "Case=Par|Number=Plur", "nsubj:cop"],
            ["polnud", "olema", "AUX", "Mood=Ind|Polarity=Neg|Tense=Past|VerbForm=Fin|Voice=Act", "cop"],
            ["ja", "ja", "CCONJ", "_", "cc"],
            ["keegi", "keegi", "PRON", "Case=Nom|Number=Sing|PronType=Ind", "nsubj"],
            ["vigastada", "vigastama", "VERB", "VerbForm=Inf", "conj"],
            ["ei", "ei", "AUX", "Polarity=Neg", "aux"],
            ["saanud", "saama", "AUX", "Connegative=Yes|Mood=Ind|Tense=Past|VerbForm=Fin|Voice=Act", "aux"],
            [".", ".", "PUNCT", "_", "punct"],
            ["Päästekeskus", "pääste_keskus", "NOUN", "Case=Nom|Number=Sing", "nsubj"],
            ["sai", "saama", "VERB", "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act", "root"],
            ["Suur–Lossi", "Suur–Loss", "PROPN", "Case=Gen|Number=Sing", "obl"],
            ["24", "24", "NUM", "Case=Gen|NumForm=Digit|NumType=Card|Number=Sing", "nummod"],
            ["asuva", "asuv", "ADJ", "Case=Gen|Degree=Pos|Number=Sing|Tense=Pres|VerbForm=Part|Voice=Act", "acl"],
            ["maja", "maja", "NOUN", "Case=Gen|Number=Sing", "nmod"],
            ["põlengust", "põleng", "NOUN", "Case=Ela|Number=Sing", "obl"],
            ["teate", "teade", "NOUN", "Case=Gen|Number=Plur", "obj"],
            ["kell", "kell", "NOUN", "Case=Nom|Number=Sing", "obl"],
            ["5.06", "5.06", "NUM", "NumForm=Digit|NumType=Card", "nummod"],
            [".", ".", "PUNCT", "_", "punct"],
            ["Kohale", "kohale", "ADV", "_", "compound:prt"],
            ["sõitsid", "sõitma", "VERB", "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin|Voice=Act", "root"],
            ["kaks", "kaks", "NUM", "Case=Nom|NumForm=Word|NumType=Card|Number=Sing", "nummod"],
            ["Haapsalu", "Haap_salu", "PROPN", "Case=Par|Number=Sing", "nsubj"],
            [",", ",", "PUNCT", "_", "punct"],
            ["kaks", "kaks", "NUM", "Case=Nom|NumForm=Word|NumType=Card|Number=Sing", "nummod"],
            ["Risti", "Rist", "PROPN", "Case=Par|Number=Sing", "conj"],
            ["ja", "ja", "CCONJ", "_", "cc"],
            ["üks", "üks", "DET", "Case=Nom|Number=Sing|PronType=Ind", "det"],
            ["Pürksi", "Pürksi", "PROPN", "Case=Gen|Number=Sing", "nmod"],
            ["päästekomando", "pääste_komando", "NOUN", "Case=Gen|Number=Sing", "nmod"],
            ["ekipaaž", "ekipaaž", "NOUN", "Case=Nom|Number=Sing", "conj"],
            [".", ".", "PUNCT", "_", "punct"],
            ["Päästjad", "päästja", "NOUN", "Case=Nom|Number=Plur", "nsubj"],
            ["said", "saama", "VERB", "Mood=Ind|Number=Plur|Person=3|Tense=Past|VerbForm=Fin|Voice=Act", "root"],
            ["tulele", "tuli", "NOUN", "Case=All|Number=Sing", "obl"],
            ["piiri", "piir", "NOUN", "Case=Gen|Number=Sing", "obj"],
            ["kl", "kl", "NOUN", "Abbr=Yes", "appos"],
            ["5.58", "5.58", "NUM", "NumForm=Digit|NumType=Card", "flat"],
            ["ja", "ja", "CCONJ", "_", "cc"],
            ["kustutustöö", "kustutus_töö", "NOUN", "Case=Nom|Number=Sing", "obj"],
            ["lõpetati", "lõpetama", "VERB", "Mood=Ind|Tense=Past|VerbForm=Fin|Voice=Pass", "conj"],
            ["kl", "kl", "NOUN", "Abbr=Yes", "obl"],
            ["9.39", "9.39", "NUM", "NumForm=Digit|NumType=Card", "nummod"],
            [".", ".", "PUNCT", "_", "punct"],
            ["Kella", "kell", "NOUN", "Case=Gen|Number=Sing", "obl"],
            ["kaheksa", "kaheksa", "NUM", "Case=Gen|NumForm=Word|NumType=Card|Number=Sing", "obl"],
            ["ajal", "ajal", "ADP", "AdpType=Post", "case"],
            ["põlengupaika", "põlengu_paik", "NOUN", "Case=Gen|Number=Sing", "obj"],
            ["jõudnud", "jõud=nud", "ADJ", "Degree=Pos|Tense=Past|VerbForm=Part|Voice=Act", "acl"],
            ["päästeteenistuse", "pääste_teenistus", "NOUN", "Case=Gen|Number=Sing", "nmod"],
            ["Haapsalu", "Haap_salu", "PROPN", "Case=Gen|Number=Sing", "nmod"],
            ["komando", "komando", "NOUN", "Case=Gen|Number=Sing", "nmod"],
            ["operatiivkorrapidaja", "operatiiv_korra_pidaja", "NOUN", "Case=Nom|Number=Sing", "nsubj"],
            ["Hannes", "Hannes", "PROPN", "Case=Nom|Number=Sing", "appos"],
            ["Kliss", "Kliss", "PROPN", "Case=Nom|Number=Sing", "flat"],
            ["ütles", "ütlema", "VERB", "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act", "root"],
            [",", ",", "PUNCT", "_", "punct"],
            ["et", "et", "SCONJ", "_", "mark"],
            ["maja", "maja", "NOUN", "Case=Gen|Number=Sing", "nmod"],
            ["sisustus", "sisustus", "NOUN", "Case=Nom|Number=Sing", "nsubj"],
            ["on", "olema", "AUX", "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act", "aux"],
            ["hävinud", "hävima", "VERB", "Tense=Past|VerbForm=Part|Voice=Act", "ccomp"],
            [".", ".", "PUNCT", "_", "punct"], ["„", "\"", "PUNCT", "_", "punct"],
            ["Õhtul", "õhtu", "NOUN", "Case=Ade|Number=Sing", "obl"],
            ["oli", "olema", "AUX", "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act", "aux"],
            ["keegi", "keegi", "PRON", "Case=Nom|Number=Sing|PronType=Ind", "nsubj"],
            ["seal", "seal", "ADV", "_", "advmod"],
            ["kütmas", "kütma", "VERB", "Case=Ine|VerbForm=Sup|Voice=Act", "xcomp"],
            ["käinud", "käima", "VERB", "Tense=Past|VerbForm=Part|Voice=Act", "root"],
            ["ja", "ja", "CCONJ", "_", "cc"],
            ["oli", "olema", "AUX", "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act", "aux"],
            ["katlale", "katlas", "NOUN", "Case=All|Number=Sing", "obl"],
            ["pilgu", "pilk", "NOUN", "Case=Gen|Number=Sing", "obj"],
            ["peale", "peale", "ADP", "AdpType=Post", "case"],
            ["heitnud", "heitma", "VERB", "Tense=Past|VerbForm=Part|Voice=Act", "conj"],
            [".", ".", "PUNCT", "_", "punct"],
            ["Kõik", "kõik", "DET", "Case=Nom|Number=Plur|PronType=Tot", "det"],
            ["märgid", "märk", "NOUN", "Case=Nom|Number=Plur", "nsubj"],
            ["näitavad", "näitama", "VERB", "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act", "root"],
            ["seda", "see", "PRON", "Case=Par|Number=Sing|PronType=Dem", "obj"],
            [",", ",", "PUNCT", "_", "punct"], ["kuid", "kuid", "CCONJ", "_", "cc"],
            ["see", "see", "PRON", "Case=Nom|Number=Sing|PronType=Dem", "nsubj:cop"],
            ["on", "olema", "AUX", "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act", "cop"],
            ["minu", "mina", "PRON", "Case=Gen|Number=Sing|Person=1|PronType=Prs", "nmod"],
            ["isiklik", "isiklik", "ADJ", "Case=Nom|Degree=Pos|Number=Sing", "amod"],
            ["arvamus", "arvamus", "NOUN", "Case=Nom|Number=Sing", "conj"],
            [",", ",", "PUNCT", "_", "punct"], ["et", "et", "SCONJ", "_", "mark"],
            ["tuli", "tulema", "VERB", "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act", "acl"],
            ["sai", "saama", "VERB", "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act", "csubj"],
            ["alguse", "algus", "NOUN", "Case=Gen|Number=Sing", "obj"],
            ["katlaruumist", "katla_ruum", "NOUN", "Case=Ela|Number=Sing", "obl"],
            ["ja", "ja", "CCONJ", "_", "cc"],
            ["kütmisest", "kütmine", "NOUN", "Case=Ela|Number=Sing", "conj"],
            [",", ",", "PUNCT", "_", "punct"],
            ["”", "”", "PUNCT", "_", "punct"],
            ["ütles", "ütlema", "VERB", "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act", "parataxis"],
            ["ta", "tema", "PRON", "Case=Nom|Number=Sing|Person=3|PronType=Prs", "nsubj"],
            ["ja", "ja", "CCONJ", "_", "cc"],
            ["toonitas", "toonitama", "VERB", "Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act", "conj"],
            [",", ",", "PUNCT", "_", "punct"],
            ["et", "et", "SCONJ", "_", "mark"],
            ["lõpliku", "lõplik", "ADJ", "Case=Gen|Degree=Pos|Number=Sing", "amod"],
            ["hinnangu", "hinnang", "NOUN", "Case=Gen|Number=Sing", "obj"],
            ["annavad", "andma", "VERB", "Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act", "ccomp"],
            ["eksperdid", "ekspert", "NOUN", "Case=Nom|Number=Plur", "nsubj"],
            ["uurimise", "uurimine", "NOUN", "Case=Gen|Number=Sing", "obl"],
            ["järel", "järel", "ADP", "AdpType=Post", "case"],
            [".", ".", "PUNCT", "_", "punct"]
        ]]

    text = Text.from_input(input_text)
    print(
        f'Teksti {text.file_id}\n'
        f'{text.sent_number}\n' # aga kuidas seda normaliseerid? lausete 
        # f'seal on {text.get_nouns()} nimisõna, normaliseeritud nimisõnade hulk {text.get_nouns()/text.normalize}, '
        # f'teksti pikkus on {text.get_text_length()}, '
        # f'ttr on {text.get_TTR()}\n'
        # f'core verbs: {text.get_core_verbs()}, non-core verbs: {text.get_non_core_verbs()}\n'
        # f'finite verbs: {text.get_finite_verbs()}\n'
        # f'infinite: {text.get_infinite_verbs()}\n'
        # f'ratio {text.get_verbtype_ratio()}\n'
        # f'{text.get_third_pron()}\n'
        # f'{text.get_genitive()}\n'
        # f'nsubje: {text.get_nsubj()}\n'
        f'koopula: {text.get_nsubj_cop()}\n'
        f'{text.get_average_word_length()}\n'
        f'{text.get_modals()}\n'
        f'hapax: {text.get_hapax_legomena()}\n'
        f'{text.get_relative_clause_modifier()}\n'
        f'{text.get_abbriviations()}\n'

    )


if __name__ == '__main__':
    main()

