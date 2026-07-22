from packager.methods import Methods
from packager.base_record import BaseRecord

def test_subjects():
    record = BaseRecord()
    record.init("archives")
    methods = Methods()
    data = ["Columbia;Willamette;Deschutes"]
    ind = 0
    assert (methods.subjects(record, data, ind)) == ["Columbia","Willamette", "Deschutes"]
