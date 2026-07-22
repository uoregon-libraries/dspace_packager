from packager.methods import Methods
from packager.base_record import BaseRecord
import datetime

def test_construct_dirname():
    record = BaseRecord()
    record.init("chc")
    record.data["email"] = {"ind": 0}
    arr = ["susannabanana@uoregon.edu"]
    assert (record.construct_methods.construct_dirname(record.data, arr)) == "susannabanana"

def test_construct_filename():
    record = BaseRecord()
    record.init("chc")
    record.data["email"] = {"ind": 0}
    arr = ["susannabanana@uoregon.edu"]
    assert (record.construct_methods.construct_filename(record.data, arr)) == "susannabanana_thesis.pdf"

def test_construct_name():
    record = BaseRecord()
    record.init("chc")
    record.data["author"] = {"ind": [0,1]}
    arr = ["susanna","banana"]
    assert (record.construct_methods.construct_name(record, arr, record.data['author']['ind'])) == "banana, susanna"

def test_subject():
    record = BaseRecord()
    record.init("chc")
    record.data["subject"] = {"ind": [0,4]}
    arr = ["gargoyle","grotesque","gothic architecture","hunky punk","chimera"]
    assert (record.construct_methods.subject(record, arr, record.data['subject']['ind'])) == ["gargoyle","grotesque","gothic architecture","hunky punk","chimera"]

def test_description():
    record = BaseRecord()
    record.init("chc")
    record.data["description"] = {"ind": 0}
    arr = ["70"]
    assert (record.construct_methods.description(record, arr, record.data['description']['ind'])) == "70 pages."

def test_embargo():
    record = BaseRecord()
    record.init("chc")
    record.data["embargo"] = {"ind": 0}
    arr = ["My advisor and I have discussed this and there are reasons that my thesis cannot be made available to the UO Campus community. Please note that a Scholars' Bank librarian will reach out to your advisor to follow up on options for archiving your thesis."]
    assert (record.construct_methods.embargo(record, arr, record.data['embargo']['ind'])) == "2145-01-01"
    arr = ["I would like to restrict the availability of my thesis file to UO Campus access only for a two year period, then have it openly available in Scholars' Bank"]
    date = record.construct_methods.embargo(record, arr, record.data['embargo']['ind'])
    y = date.split("-")[0]
    assert (int(y)-2) == datetime.datetime.now().year
    arr = ["I would like my thesis file to be openly available in Scholars' Bank"]
    assert (record.construct_methods.embargo(record, arr, record.data['embargo']['ind'])) == ""
