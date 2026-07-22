from base_record import BaseRecord
import re

class FullRecord(BaseRecord):

    def __init__(self):
        super().__init__()
        self.dirname = {}
        self.contributor = {}
        self.title_alt = {}
        self.identifier_other = {}

    def set_metadata(self, tsv_string: str) -> list[str]:
        arr = super().set_metadata(tsv_string)
        self.description['val'] = arr[self.description['ind']]
        self.filename['val'] = self.construct_filename(arr)
        self.dirname['val'] = self.construct_dirname(arr)
        self.subjects['val'] = self.construct_subjects(arr)
        self.issued['val'] = arr[self.issued['ind']]
        self.title_alt['val'] = self.char_handler.clean(arr[self.title_alt['ind']])
        return arr

    def construct_filename(self, arr: list[str]) -> str:
        fname = arr[self.filename['ind']]
        p = re.compile('[a-zA-Z0-9._-]*')
        clean = p.match(fname)
        if clean.group() != fname:
            raise ValueError(f"Filename is not clean: {fname}")
        return fname

    def construct_dirname(self, arr: list[str]) -> str:
        return arr[self.filename['ind']].replace(".pdf", "")

    def construct_subjects(self, arr: list[str]) -> list[str]:
        subjects = []
        subj_str = arr[self.subjects['ind']]
        subs = subj_str.strip().split(";")
        for sub in subs:
          subjects.append(self.char_handler.clean(sub.strip()))
        return subjects

    def assemble_properties(self) -> str:
        string = self.dc_formatter.begin_xml()
        string += super().assemble_properties()
        
        string += self.dc_formatter.contributor(self.contributor.get('val'))
        string += self.dc_formatter.title_alt(self.title_alt.get('val'))
        string += self.dc_formatter.identifier_other(self.identifier_other.get('val'))
        string += self.dc_formatter.end_xml()
        return string
