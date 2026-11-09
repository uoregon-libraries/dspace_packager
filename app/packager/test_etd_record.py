from packager.etd_record import EtdRecord
import os

def test_assemble_colls():
  projpath = "/Users/lsato/dspace_packager/app/packager"
  record = EtdRecord()
  record.init("etds")
  record.import_config(os.path.join(projpath, "etds/fixtures/config"))
  record.data['department']['val'] = 'Classics'
  assert(record.assemble_colls()) == "1794/13076\n1794/6008\n"

def test_set_metadata():
  projpath = "/Users/lsato/dspace_packager/app/packager"
  record = EtdRecord()
  record.init("etds")
  record.import_config(os.path.join(projpath, "etds/fixtures/config"))
  record.set_metadata(os.path.join(projpath, "etds/fixtures/test_DATA.xml"))
  assert record.data['title']['val'] == "What Do We Know And When Did We Know It"
  assert record.data['orcid']['val'] == "0000-1111-2222-3333"
  assert record.data['degree']['val'] == "Ph.D."
  assert record.data['department']['val'] == "Department of Psychology"
  assert record.data['institution']['val'] == "University of Oregon"

def test_assemble_degree_properties():
  expected = '<?xml version="1.0" ?><dublin_core schema="degree"><dcvalue element="degree" qualifier="name">Ph.D.</dcvalue><dcvalue element="degree" qualifier="discipline">Department of Psychology</dcvalue><dcvalue element="degree" qualifier="grantor">University of Oregon</dcvalue><dcvalue element="degree" qualifier="level">doctoral</dcvalue></dublin_core>'
  projpath = "/Users/lsato/dspace_packager/app/packager"
  record = EtdRecord()
  record.init("etds")
  record.import_config(os.path.join(projpath, "etds/fixtures/config"))
  record.set_metadata(os.path.join(projpath, "etds/fixtures/test_DATA.xml"))
  assert(record.assemble_degree_properties()) == expected