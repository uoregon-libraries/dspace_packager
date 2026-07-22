from packager.methods import Methods
import re

# Processing methods for archives packages
class ProjectMethods(Methods):

    def construct_filename(self, record, data) -> str:
        fname = data[record['filename']['ind']]
        p = re.compile('[a-zA-Z0-9._-]*')
        clean = p.match(fname)
        if clean.group() != fname:
            raise ValueError(f"Filename is not clean: {fname}")
        return fname

    def construct_dirname(self, record, data) -> str:
        return data[record['filename']['ind']].replace(".pdf", "")

    # for archives colls, always true
    def construct_permission(self, record, data) -> bool:
        return True
