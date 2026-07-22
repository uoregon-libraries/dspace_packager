from base_record import BaseRecord
import re

class FullRecord(BaseRecord):

    def __init__(self):
        super().__init__()
        self.advisors = {}
        self.dirname = {}

    def set_metadata(self, tsv_string: str) -> list[str]:
        arr = super().set_metadata(tsv_string)
        self.authors['val'] = [self.char_handler.clean(arr[self.authors['ind']])]
        self.advisors['val'] = self.construct_advisors(arr)
        self.abstract['val'] = self.char_handler.clean(arr[self.abstract['ind']])
        self.description['val'] = arr[self.page_count['ind']] + " pages."
        self.filename['val'] = self.construct_filename(arr)
        self.dirname['val'] = self.construct_dirname(arr)
        self.subjects['val'] = self.construct_subjects(arr)
        self.issued['val'] = arr[self.issued['ind']]
        return arr

    def construct_filename(self, arr: list[str]) -> str:
        fname = arr[self.filename['ind']]
        p = re.compile('[a-zA-Z0-9_-]*')
        clean = p.match(fname)
        if clean.group() != fname:
            raise ValueError(f"Filename is not clean: {fname}")
        return fname + ".pdf"

    def construct_dirname(self, arr: list[str]) -> str:
        return arr[self.filename['ind']]

    def construct_advisors(self, arr: list[str]) -> list[str]:
        advisors = []
        advisors.append(self.char_handler.clean(arr[self.advisors['ind'][0]]))
        if  arr[self.advisors['ind'][1]] != "":
          advisors.append(self.char_handler.clean(arr[self.advisors['ind'][1]]))
        return advisors

    def construct_subjects(self, arr: list[str]) -> list[str]:
        subjects = []
        subj_str = arr[self.subjects['ind']]
        subs = subj_str.strip().split(",")
        for sub in subs:
          subjects.append(self.char_handler.clean(sub.strip()))
        return subjects

    def addl_rights(self) -> str:
      return "UO theses and dissertations are provided for research and educational purposes and may be under copyright by the author or the author’s heirs. Please contact scholars@uoregon.edu with any questions or comments. In your email, be sure to include the URL and title of the specific items that you are inquiring about."

    def assemble_properties(self) -> str:
        string = self.dc_formatter.begin_xml()
        string += super().assemble_properties()
        
        for author in self.authors.get('val', []):
            string += self.dc_formatter.author(author)
        
        for advisor in self.advisors.get('val', []):
            string += self.dc_formatter.advisor(advisor)

        string += self.dc_formatter.rights(self.addl_rights())

        string += self.dc_formatter.end_xml()
        return string
