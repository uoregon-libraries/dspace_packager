from packager.methods import Methods
import datetime

class ProjectMethods(Methods):

    def construct_dirname(self, record, data) -> str:
        return data[record['email']['ind']].replace("@uoregon.edu", "")

    def construct_filename(self, record, data) -> str:
        return data[record['email']['ind']].replace("@uoregon.edu", "_thesis.pdf")

    def construct_permission(self, record, data) -> bool:
        return data[record['permission']['ind']].strip().lower() == 'yes'

    # ind has indices of first and last names
    def construct_name(self, record, data, ind) -> str:
        last_name = record.char_handler.clean(data[ind[1]])
        first_name = record.char_handler.clean(data[ind[0]])
        return(f"{last_name}, {first_name}")

    def subject(self, record, data, ind) -> list[str]:
      subjects = []
      start, end = ind
      for i in range(start, end + 1):
        if i < len(data):
          subjects.append(record.char_handler.clean(data[i]))
      return subjects

    def description(self, record, data, ind) -> str:
        return data[ind] + " pages."

    def embargo(self, record, data, ind) -> str:
        # print(f"processing embargo: {arr[self.embargo['ind']].lower()}...")
        """
        Original logic for 2-year embargo.
        Note: The `construct_forever_embargo` is used in `set_metadata`.
        """
        if 'two year' in data[ind].lower():
            return self.add2Y()
        if 'openly' in data[ind].lower():
            return ""
        return "2145-01-01"

    def construct_forever_embargo(self, record, data, ind) -> str:
        if 'permanently restrict' in data[ind].lower():
            return "2145-01-01"
        return ""

    def add2Y(self) -> str:
        """Returns a date string for 2 years in the future."""
        d = datetime.datetime.now()
        try:
            # Safely add 2 years, handles leap years
            d2 = d.replace(year=d.year + 2)
        except ValueError:
            # Handles Feb 29 on a leap year
            d2 = d.replace(year=d.year + 2, day=d.day - 1)
        return d2.strftime('%Y-%m-%d')

