from packager.methods import Methods
from packager.etd_record import EtdRecord
import os
import xml.etree.ElementTree as ET

def test_construct_methods():
  projpath = "/Users/lsato/dspace_packager/app/packager"
  xml_path = os.path.join(projpath, "etds/fixtures/test_DATA.xml")
  root = ET.parse(xml_path).getroot()
  record = EtdRecord()
  record.init("etds")
  abstract = "'Twas brillig, and the slithy toves Did gyre and gimble in the wabe: All mimsy were the borogoves, And the mome raths outgrabe.\n\n&quot;Beware the Jabberwock, my son! The jaws that bite, the claws that catch! Beware the Jubjub bird, and shun The frumious Bandersnatch!&quot;\n\nHe took his vorpal sword in hand; Long time the manxome foe he sought- So rested he by the Tumtum tree And stood awhile in thought.\n\nAnd, as in uffish thought he stood, The Jabberwock, with eyes of flame, Came whiffling through the tulgey wood, And burbled as it came!"
  assert (record.construct_methods.construct_author(root)) == "Hatsune, Miku"
  assert (record.construct_methods.construct_advisor(root)) == "Pfeifer, Jennifer"
  assert(record.construct_methods.construct_embargo(root)) == "2028-07-31"
  assert(record.construct_methods.construct_license(root)) == "CC BY"
  assert(record.construct_methods.construct_level(root)) == "doctoral"
  assert(record.construct_methods.construct_abstract(root)) == abstract
  assert(record.construct_methods.construct_subject(root)) == ["anxiety", "depression", "internalizing", "longitudinal", "mentalizing", "self"]
