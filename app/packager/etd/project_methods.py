from packager.methods import Methods
from datetime import datetime
import xml.etree.ElementTree as ET
import html
from pathlib import Path
from packager.helpers import SpecialChars
import re

class ProjectMethods(Methods):

  def __init__(self):
    self.char_handler = SpecialChars()

  def find_element_text(self, root, path, special_convert=False):
    """Helper to find text in XML, with optional special chars conversion."""
    text = root.findtext(path, default='').strip()
    return self.char_handler.clean(text) if special_convert else text

  def construct_dirname(self, root) -> str:
    #name = Path(name).stem
    name = self.find_element_text(root, 'DISS_content/DISS_binary')
    return name.replace(".pdf", "")

  def construct_abstract(self, root) -> str:
    abstract_pars = [self.char_handler.clean(self.strip_tags(p.text)) for p in root.findall('DISS_content/DISS_abstract/DISS_para')]
    abstract = "\n\n".join(abstract_pars)
    return abstract

  def construct_author(self, root) -> str:
    surname = self.find_element_text(root, 'DISS_authorship/DISS_author/DISS_name/DISS_surname')
    fname = self.find_element_text(root, 'DISS_authorship/DISS_author/DISS_name/DISS_fname')
    return self.char_handler.clean(f"{surname}, {fname}")

  def construct_advisor(self, root) -> str:
    adv_surname = self.find_element_text(root, 'DISS_description/DISS_advisor/DISS_name/DISS_surname')
    adv_fname = self.find_element_text(root, 'DISS_description/DISS_advisor/DISS_name/DISS_fname')
    return self.char_handler.clean(f"{adv_surname}, {adv_fname}")

  def construct_level(self, root) -> str:
    return root.find('DISS_description').get('type', '')

  def construct_license(self, root) -> str:
    val = self.find_element_text(root, 'DISS_creative_commons_license/DISS_abbreviation')
    return 'All Rights Reserved.' if val == 'none' else val

  def construct_subject(self, root) -> list:
    vals = self.find_element_text(root, 'DISS_description/DISS_categorization/DISS_keyword').split(',')
    subjects = []
    for val in vals:
      subjects.append(self.char_handler.clean(val.strip()))
    return subjects

  def construct_embargo(self, root) -> str:
    code = self.get_embargo_code(root)
    raw = self.get_sales_release(root)
    if code == '0':
      if raw != '':
        raise error
      else:
        return ''
    else:
      return self.reformat_date(raw)

  def is_embargo_present(self, xml_root):
    """Checks for presence of an embargo in the XML."""
    # 1. Check embargo_code attribute
    if xml_root.get('embargo_code') != '0':
        return True
    # 2. Check DISS_delayed_release element
    if xml_root.findtext('DISS_repository/DISS_delayed_release', '').strip():
        return True
    # 3. Check DISS_access_option element
    access_option = xml_root.findtext('DISS_repository/DISS_access_option', '').strip()
    if access_option and 'open' not in access_option.lower():
        return True
    return False

  def validate_date(self, date_str):
    """Validates a date in yyyy-mm-dd format."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False

  def reformat_date(self, date_str):
    """Converts MM/DD/YYYY to YYYY-MM-DD and validates the date."""
    if not date_str:
        return None
    try:
        # strptime validates the date, e.g., it will fail for "02/30/2023"
        dt = datetime.strptime(date_str, '%m/%d/%Y')
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        return None

  def get_embargo_code(self, xml_root):
    """Extracts the embargo_code attribute from the XML root."""
    return xml_root.get('embargo_code', '')


  def get_sales_release(self, xml_root):
    """Extracts the sales release date from the XML."""
    # Path to the element: DISS_restriction/DISS_sales_restriction
    sales_restriction_element = xml_root.find('DISS_restriction/DISS_sales_restriction')
    if sales_restriction_element is not None:
        return sales_restriction_element.get('remove', '')
    return ''

  def strip_tags(self, text) -> str:
    """Removes <i>, <sub>, <sup> tags, both as <tag> and &lt;tag&gt;."""
    if not text:
        return ""
    # This single regex handles all cases from the original PHP script
    pattern = re.compile(r'(&lt;|<)/?(italic|sub|super)(&gt;|>)', re.IGNORECASE)
    return pattern.sub('', text)
