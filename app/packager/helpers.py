from datetime import datetime
from xml.sax.saxutils import escape
import shutil
import datetime
import os

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

    def issued(self, date: str) -> str:
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

def zip_proj_dirs(proj):

    pkg_dirs = []
    for root, dirs, files in os.walk(f'instance/{proj}/work'):
        pkg_dirs.extend(dirs)
        break
    datestring = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    zip_dir = f"instance/{proj}/zips/{datestring}"
    os.makedirs(zip_dir)
    for d in pkg_dirs:
        output_path = os.path.join(zip_dir, f'{d}')
        folder_path = f'instance/{proj}/work/{d}'
        shutil.make_archive(output_path, 'zip', folder_path)
