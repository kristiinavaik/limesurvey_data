import csv
import json

from collections import defaultdict
from typing import List
from pathlib import Path

"""
Sisend: eelnevalt genereeritud dimensioonide failid (12tk), kus igal real on ühe hindaja vastused kujul (tekst1, tekst2, ümbertehtud skoor)
Väljund: tulemsued lähevad tabelisse, kus ridadeks on teksti paarid (tekst1; tekst2) ja veergudes hindajad. Skoor on kas 01, 1 või 0.
"""


def leia_tulemuste_failid() -> List[Path]:
    tulemuste_dir = Path('dimensioonide_vastused')
    return [p for p in tulemuste_dir.glob('*') if p.suffix != '.json']


class Processor:

    def __init__(self, paths):
        self._paths = paths
        self.vastused = None

    def _initsialiseeri_vastused(self):
        self.vastused = defaultdict(dict)  # { (t1, t2): {id1: hinne1, id2: hinne2}, ... }

    def save_json(self, path):
        d = {}
        for k, v in self.vastused.items():
            d[','.join(k)] = v
        with open(path, 'w') as f:
            json.dump(d, f, indent=4)

    def _parse_line(self, line: str):
        vastaja_id, limesurvey_vastused = line.split(';')
        vastused = limesurvey_vastused[2:-2].split('), (')
        for v in vastused:
            t1, t2, hinne = v.lstrip('(').rstrip(')').split(', ')
            try:
                int(hinne)
            except ValueError:
                raise ValueError(v, vastused)
            teksti_paar = (t1, t2)
            self.vastused[teksti_paar][vastaja_id] = hinne.rstrip(')')

    def _process_path(self, path: Path):
        with path.open() as fd:
            for line in fd:
                self._parse_line(line)

    def _leia_vastajate_ids(self, exclude_ids=None) -> List[str]:
        vastajad = set()
        for vastused in self.vastused.values():
            vastajad.update(vastused.keys())
        vastajate_ids = sorted(vastajad, key=lambda v: int(v.split('_')[-1]))
        return [_id for _id in vastajate_ids if _id not in (exclude_ids or [])]

    def _genereeri_tabel(self) -> List[dict]:
        vastajad = self._leia_vastajate_ids()
        tabel = []
        for teksti_paar, vastused in self.vastused.items():
            rida = {'teksti_paar': ' | '.join(teksti_paar)}
            for vastaja in vastajad:
                rida[vastaja] = vastused.get(vastaja, '#')
            tabel.append(rida)
        return tabel

    def process(self, with_headers=True, exclude_ids=None):
        for path in self._paths:
            self._initsialiseeri_vastused()
            print(f'Processing path {path}')
            self._process_path(path)
            tabel = self._genereeri_tabel()
            csv_name = f'tulemused_tabelis/{path.name}.csv'
            self.save_csv(tabel, csv_name, with_headers=with_headers, exclude_ids=exclude_ids)
            print(f'Tulemused {path} => {csv_name}')

    def save_csv(self, tabel: List[dict], path, with_headers=True, exclude_ids=None):
        vastajate_ids = self._leia_vastajate_ids(exclude_ids=exclude_ids)
        if with_headers:
            field_names = ['teksti_paar', *vastajate_ids]
        else:
            field_names = vastajate_ids
        with open(path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            if with_headers:
                writer.writeheader()
            for rida in tabel:
                if with_headers:
                    headers = ['teksti_paar']
                    csv_line = rida
                else:
                    headers = []
                headers.extend(vastajate_ids)
                csv_line = {k: v for k, v in rida.items() if k in headers}
                writer.writerow(csv_line)


def main():
    paths = leia_tulemuste_failid()
    processor = Processor(paths)
    exclude_ids = None
    # exclude_ids = ('ID_10',)
    processor.process(with_headers=False, exclude_ids=exclude_ids)


if __name__ == '__main__':
    main()
