import pdb

# This class meant to hold processing methods that will apply broadly to any project
class Methods:

    # data is an array, assumes the subject is a single string with separator
    def subjects(self, record, data, ind) -> list:
        subjects = []
        subs = data[ind].strip().split(";")
        for sub in subs:
            subjects.append(record.char_handler.clean(sub.strip()))
        return subjects
