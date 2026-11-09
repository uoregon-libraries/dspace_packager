import xml.etree.ElementTree as ET
import re
import html
from packager.base_record import BaseRecord
import packager.deptlookup

class EtdRecord(BaseRecord):

  def set_metadata(self, xmlpath: str):
    root = ET.parse(xmlpath).getroot()

    self.data['title']['val'] = self.find_element_text(root, 'DISS_description/DISS_title', True)
    self.data['orcid']['val'] = self.find_element_text(root, 'DISS_authorship/DISS_author/DISS_orcid')
    self.data['author']['val'] = self.construct_methods.construct_author(root)
    self.data['advisor']['val'] = self.construct_methods.construct_advisor(root)
    self.data['degree']['val'] = self.find_element_text(root, 'DISS_description/DISS_degree')
    self.data['department']['val'] = self.find_element_text(root, 'DISS_description/DISS_institution/DISS_inst_contact')
    self.data['subject']['val'] = self.construct_methods.construct_subject(root)
    self.data['abstract']['val'] = self.construct_methods.construct_abstract(root)
    self.data['embargo']['val'] = self.construct_methods.construct_embargo(root)
    self.data['level']['val'] = self.construct_methods.construct_level(root)
    self.data['institution']['val'] = self.find_element_text(root, 'DISS_description/DISS_institution/DISS_inst_name')
    self.data['license']['val'] = self.construct_methods.construct_license(root)
    self.filename = self.find_element_text(root, 'DISS_content/DISS_binary')
    self.dirname = self.construct_methods.construct_dirname(root)
    self.permission = True
    del self.data['permission']

  def assemble_degree_properties(self) -> str:
    string = self.dc_formatter.begin_degree_xml()
    string += self.dc_formatter.deg_degree(self.data['degree']['val'])
    string += self.dc_formatter.deg_dept(self.data['department']['val'])
    string += self.dc_formatter.deg_inst(self.data['institution']['val'])
    string += self.dc_formatter.deg_level(self.data['level']['val'])
    string += self.dc_formatter.end_xml()
    return string

  def assemble_colls(self):
    content = "1794/13076\n"
    dept_code = packager.deptlookup.lookupcode(self.data['department']['val'])
    if dept_code.strip():
      content += f"1794/{dept_code}\n"
    return content

  def find_element_text(self, root, path, special_convert=False):
    """Helper to find text in XML, with optional special chars conversion."""
    text = root.findtext(path, default='').strip()
    return self.char_handler.clean(text) if special_convert else text

    def set_filename(self, arr: list):
        self.filename = self.construct_methods.construct_filename(self.data, arr)

    def set_dirname(self, arr: list):
        self.dirname = self.construct_methods.construct_dirname(self.data, arr)

    def set_permission(self, arr: list):
        self.permission = True
