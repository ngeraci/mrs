""" Example of using Mrs. library to create a CSV report
    listing flagged names and their frequency of occurence
    in the source data.

    In this example, the names written out to the report are
    ones that match the format "Mrs. [Firstname] [Lastname],"
    where the first name's gender guesser value is not "female"
    or "mostly_female".

"""

import csv
from collections import Counter
from itertools import chain
import mrs

def main():

    create_report("data/mrs_test_data.csv", "data/sample_report.csv")

def create_report(infile_path, outfile_path):

    with open(infile_path, "r") as infile:
        reader = csv.reader(infile)
        # read rows to flat list
        row_list = list(chain.from_iterable(row for row in reader))
        # join non-blank list items to string
        input_string = ", ".join([x for x in row_list if x])

    flagged_names = []
    data = mrs.Text(input_string)
    for entity in data.mrs_names:
        name = mrs.Name(entity)
        if name.format == "first_last":
            if name.gender_guess not in ["female", "mostly_female"]:
                flagged_names.append("Mrs. " + name.text)
        elif name.gender_guess == "initials":
            flagged_names.append("Mrs. " + name.text)

    #most_common sorts counter by value
    name_count = Counter(flagged_names).most_common()

    with open(outfile_path, "w", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["Name", "Frequency"])
        writer.writeheader()
        for name in name_count:
            writer.writerow({"Name": name[0], "Frequency": name[1]})


if __name__ == "__main__":
    main()
