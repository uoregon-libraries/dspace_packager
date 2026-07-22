from base_record import BaseRecord

class FullRecord(BaseRecord):

    def __init__(self):
        super().__init__()
        self.advisor_first = {}
        self.advisor_last = {}
        self.author_first = {}
        self.author_last = {}
        self.authors = {}
        self.advisors = {}
        self.orcid = {}
        self.embargo = {}
        self.dirname = {}
        self.email = {}

    def set_metadata(self, tsv_string: str) -> list[str]:
        arr = super().set_metadata(tsv_string)
        self.authors['val'] = self.construct_authors(arr)
        self.advisors['val'] = self.construct_advisors(arr)
        self.abstract['val'] = self.char_handler.clean(arr[self.abstract['ind']])
        self.description['val'] = arr[self.page_count['ind']] + " pages."
        self.issued['val'] = self.issued.get('val')
        self.email['val'] = arr[self.email['ind']]
        self.filename['val'] = self.construct_filename()
        self.dirname['val'] = self.construct_dirname()

        # Check if orcid index exists and is within bounds
        if 'ind' in self.orcid and self.orcid['ind'] < len(arr):
            self.orcid['val'] = arr[self.orcid['ind']]
        else:
            self.orcid['val'] = ""
        
        # Check if rights index exists and is within bounds
        if 'ind' in self.rights and self.rights['ind'] < len(arr):
            self.rights['val'] = arr[self.rights['ind']]
        else:
            self.rights['val'] = ""

        self.embargo['val'] = self.construct_embargo(arr)
        return arr

    def construct_dirname(self) -> str:
        if not self.email.get('val'):
            return ""
        return self.email['val'].replace("@uoregon.edu", "")

    def construct_filename(self) -> str:
        if not self.email.get('val'):
            return ""
        return self.email['val'].replace("@uoregon.edu", "_thesis.pdf")

    def construct_authors(self, arr: list[str]) -> list[str]:
        authors = []
        if 'ind' in self.author_first and 'ind' in self.author_last:
                    last_name = self.char_handler.clean(arr[self.author_last['ind']])
                    first_name = self.char_handler.clean(arr[self.author_first['ind']])
                    authors.append(f"{last_name}, {first_name}")
        return authors

    def construct_advisors(self, arr: list[str]) -> list[str]:
        advisors = []
        if 'ind' in self.advisor_first and 'ind' in self.advisor_last:
                    last_name = self.char_handler.clean(arr[self.advisor_last['ind']])
                    first_name = self.char_handler.clean(arr[self.advisor_first['ind']])
                    advisors.append(f"{last_name}, {first_name}")
        return advisors

    def assemble_properties(self) -> str:
        string = self.dc_formatter.begin_xml()
        string += super().assemble_properties()
        
        for author in self.authors.get('val', []):
            string += self.dc_formatter.author(author)
        
        for advisor in self.advisors.get('val', []):
            string += self.dc_formatter.advisor(advisor)
            
        string += self.dc_formatter.embargo(self.embargo.get('val'))
        string += self.dc_formatter.orcid(self.orcid.get('val'))
        string += self.dc_formatter.end_xml()
        return string

    def construct_embargo(self, arr: list[str]) -> str:
        # print(f"processing embargo: {arr[self.embargo['ind']].lower()}...")
        """
        Original logic for 2-year embargo.
        Note: The `construct_forever_embargo` is used in `set_metadata`.
        """
        if 'ind' in self.embargo:
            if not 'restrict' in arr[self.embargo['ind']].lower():
                return ""
            if 'two year' in arr[self.embargo['ind']].lower():
                return self.add2Y()
            return self.construct_forever_embargo(arr)

    def construct_forever_embargo(self, arr: list[str]) -> str:
        """
        If 'restrict' is in the embargo field, return '9999'.
        """
        if 'ind' in self.embargo:
            if 'permanently restrict' in arr[self.embargo['ind']].lower():
                return "2145-01-01"
        return ""
