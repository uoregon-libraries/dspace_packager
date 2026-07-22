import json
from datetime import datetime
from xml.sax.saxutils import escape

class SpecialChars:
    """
    Handles special character cleaning, especially for XML output.
    """
    def clean(self, s: str) -> str:
        """
        Cleans a string by stripping whitespace, escaping special XML characters,
        and converting non-ASCII characters to numeric entities.
        """
        if not isinstance(s, str):
            return ''
        s = s.strip()
        # Escape special XML characters and quotes. The original PHP used ENT_COMPAT,
        # which escapes double quotes but not single quotes.
        s = escape(s, {'"': "&quot;"})
        # Convert non-ASCII characters to numeric character references.
        # This is a modern and simpler equivalent of the complex entity conversion in the PHP code.
        return s.encode('ascii', 'xmlcharrefreplace').decode('utf-8')

class DublinCoreXML:
    """
    Generates Dublin Core XML elements as strings.
    """
    def _dc_element(self, element: str, qualifier: str = None, language: str = None, value: str = None) -> str:
        """Helper to create a DC element string."""
        if not value:
            return ""
        
        attrs = f'element="{element}"'
        if qualifier:
            attrs += f' qualifier="{qualifier}"'
        if language:
            attrs += f' language="{language}"'
            
        return f'<dcvalue {attrs}>{value}</dcvalue>'

    def title(self, title: str) -> str:
        return self._dc_element("title", qualifier="none", value=title)

    def title_alt(self, title: str) -> str:
        return self._dc_element("title", qualifier="alternative", value=title)

    def identifier_other(self, identi: str) -> str:
        return self._dc_element("identifier", qualifier="other", value=identi)

    def author(self, author: str) -> str:
        return self._dc_element("contributor", qualifier="author", value=author)

    def advisor(self, advisor: str) -> str:
        return self._dc_element("contributor", qualifier="advisor", value=advisor)

    def contributor(self, contributor: str) -> str:
        return self._dc_element("contributor", value=contributor)

    def description(self, descrip: str) -> str:
        return self._dc_element("description", value=descrip)

    def identifier(self, identi: str) -> str:
        return self._dc_element("identifier", value=identi)

    def coverage(self, cov: str) -> str:
        return self._dc_element("coverage", qualifier="spatial", language="en_US", value=cov)

    def publisher(self, pub: str) -> str:
        return self._dc_element("publisher", qualifier="none", value=pub)

    def issuedate(self, date: str) -> str:
        return self._dc_element("date", qualifier="issued", value=date)

    def submitted(self, date: str) -> str:
        return self._dc_element("date", qualifier="submitted", value=date)

    def published(self, date: str) -> str:
        return self._dc_element("date", qualifier="published", value=date)

    def subject(self, subject: str) -> str:
        return self._dc_element("subject", qualifier="none", language="en_US", value=subject)

    def type(self, type_: str) -> str:
        return self._dc_element("type", qualifier="none", value=type_)

    def lang(self, lang_: str) -> str:
        return self._dc_element("language", qualifier="iso", value=lang_)

    def rights(self, rights_: str) -> str:
        return self._dc_element("rights", qualifier="none", value=rights_)

    def source(self, source_: str) -> str:
        return self._dc_element("source", qualifier="none", value=source_)

    def abstract(self, abstract_: str) -> str:
        return self._dc_element("description", qualifier="abstract", language="en_US", value=abstract_)

    def ispartofseries(self, series: str) -> str:
        return self._dc_element("relation", qualifier="ispartofseries", value=series)

    def orcid(self, orcid_: str) -> str:
        return self._dc_element("identifier", qualifier="orcid", value=orcid_)

    def sponsor(self, sponsor_: str) -> str:
        return self._dc_element("description", qualifier="sponsorship", value=sponsor_)

    def format(self, format_: str) -> str:
        return self._dc_element("format", qualifier="mimetype", value=format_)

    def embargo(self, date: str) -> str:
        return self._dc_element("description", qualifier="embargo", language="en_US", value=date)

    def begin_xml(self) -> str:
        return '<?xml version="1.0" ?><dublin_core schema="dc">'

    def end_xml(self) -> str:
        return '</dublin_core>'

class BaseRecord:
    """
    Represents a generic record with metadata, configurable via a JSON file.
    """
    def __init__(self):
        self.project_type = None
        self.title = {}
        self.authors = {}
        self.subjects = {}
        self.issued = {}
        self.filename = {}
        self.type = {}
        self.publisher = {}
        self.rights = {}
        self.permission = {}
        # These fields are not declared in the PHP class but are used,
        # likely populated from the config file.
        self.description = {}
        self.page_count = {}
        self.lang = {}
        self.abstract = {}
        
        self.dc_formatter = None
        self.char_handler = None

    def init(self, project_type: str):
        """Initializes the record for a specific project type."""
        self.project_type = project_type
        self.dc_formatter = DublinCoreXML()
        self.char_handler = SpecialChars()

    def set_metadata(self, tsv_string: str) -> list[str]:
        """
        Parses a tab-separated string to set metadata fields.
        Returns the parsed array.
        """
        arr = tsv_string.split("\t")
        # todo: move this check to full record
        if 'ind' in self.permission and arr[self.permission['ind']].strip().lower() != 'yes':
            raise Exception("Permission to publish is not granted.")
        
        self.title['val'] = self.char_handler.clean(arr[self.title['ind']])
        self.subjects['val'] = self.construct_subjects(arr)
        # The original returns the array, so we do too.
        return arr

    def get_configs(self):
        """Loads configuration from a JSON file based on project type."""
        config_path = f"{self.project_type}/config"
        try:
            with open(config_path, 'r') as f:
                configs = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found at {config_path}")

        for key, val in configs.items():
            if hasattr(self, key):
                current_attr = getattr(self, key)
                if isinstance(current_attr, dict):
                    current_attr.update(val)

    def construct_description(self) -> str:
        """Constructs the description string."""
        pages_val = self.pages.get('val', '')
        return f"{pages_val} pages" if pages_val else ""

    def construct_subjects(self, arr: list[str]) -> list[str]:
        """Constructs a list of subjects from the parsed data array."""
        subjects = []
        if 'ind' in self.subjects and isinstance(self.subjects['ind'], list) and len(self.subjects['ind']) == 2:
            start, end = self.subjects['ind']
            for i in range(start, end + 1):
                if i < len(arr):
                    subjects.append(self.char_handler.clean(arr[i]))
        return subjects

    def add2Y(self) -> str:
        """Returns a date string for 2 years in the future."""
        d = datetime.now()
        try:
            # Safely add 2 years, handles leap years
            d2 = d.replace(year=d.year + 2)
        except ValueError:
            # Handles Feb 29 on a leap year
            d2 = d.replace(year=d.year + 2, day=d.day - 1)
        return d2.strftime('%Y-%m-%d')

    def assemble_properties(self) -> str:
        """Assembles a string of all Dublin Core properties."""
        # Using .get('val') to avoid KeyErrors if 'val' is not set.
        parts = [
            self.dc_formatter.title(self.title.get('val')),
            self.dc_formatter.issuedate(self.issued.get('val')),
        ]
        for subject in self.subjects.get('val', []):
            parts.append(self.dc_formatter.subject(subject))
            
        parts.extend([
            self.dc_formatter.description(self.description.get('val')),
            self.dc_formatter.publisher(self.publisher.get('val')),
            self.dc_formatter.type(self.type.get('val')),
            self.dc_formatter.rights(self.rights.get('val')),
            self.dc_formatter.lang(self.lang.get('val')),
            self.dc_formatter.abstract(self.abstract.get('val')),
        ])
        
        return "".join(part for part in parts if part)
