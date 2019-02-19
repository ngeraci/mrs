# mrs

This is an experiment in creating a Python library designed to detect names of people with the structure "Mrs. \[male first name\] \[last name\]," such as "Mrs. Ralph Mayer" or "Mrs. Tomás Rivera." It uses [spaCy](https://spacy.io/) and [gender-guesser](https://pypi.org/project/gender-guesser/). 

It comes out of a library and archives metadata context, where dated descriptions don't always align with current modes of address. The goal is to flag potential instances where women were not identified by their own names, in order to target those instances for human review, revision and further research where needed. 

To view a sample report generated with this code, see [sample_report.csv](https://github.com/ngeraci/mrs_names/blob/master/data/sample_report.csv)The test data in [mrs_text_data.csv](https://github.com/ngeraci/mrs_names/blob/master/data/mrs_test_data.csv) comes from legacy metadata from the [Avery E. Field photographs](https://calisphere.org/collections/92/).

This is a work in progress, written as an exploratory experiment by someone who is primarily a metadata librarian rather than a developer.

## Usage
```python
import mrs

data = mrs.Text(input_string)

flagged_names = []
for entity in data.mrs_names:
    name = mrs.Name(entity)
    if name.format == "first_last":
        if name.gender_guess not in ["female", "mostly_female"]:
            flagged_names.append("Mrs. " + name.text)

```
For a complete example of analyzing a tabular metadata file and creating a CSV report, see [example.py](https://github.com/ngeraci/mrs_names/blob/master/example.py).