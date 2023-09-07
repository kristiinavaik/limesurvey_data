import pathlib
from typing import Generator, Tuple, Dict

"""
See skript genereerib igale dimensioonile ja igale dimensiooni tasemele (S/M, W ja NE) eraldi csv-failid.
Selle sisend on tunnuste eraldamise skripti väljund ja selle skripti tulemus on get_statistics.py sisendiks!
"""

def read_results() -> Tuple[str, Dict[str, str]]:
    with open('limesurvey_tunnuste_skoorid_070923.csv') as f:
        header = f.readline()
        results = {line.split(';', maxsplit=1)[0]: line for line in f}
    return header, results


def iter_dim_groups_files() -> Generator[pathlib.Path, None, None]:
    root = pathlib.Path('dimensioonide_grupid')
    yield from root.rglob("*_ls")


def process_ls_file(ls_file: pathlib.Path, header: str, results: Dict[str, str]) -> pathlib.Path:
    contents = ls_file.read_text().strip()
    file_ids = [file_id_with_suffix.removesuffix('.txt') for file_id_with_suffix in contents.split(',')]
    result_path = ls_file.with_name(ls_file.stem.removesuffix('_ls')).with_suffix('.csv')
    with result_path.open('w') as f:
        f.write(header)
        for file_id in file_ids:
            f.write(results[file_id])
    return result_path


def main():
    header, limesurvey_results = read_results()
    for ls_file in iter_dim_groups_files():
        print(ls_file, '=>', end=' ')
        csv_path = process_ls_file(ls_file, header, limesurvey_results)
        print(csv_path)


if __name__ == '__main__':
    main()
