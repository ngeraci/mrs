# mrs

This is an experiment in creating a Python library designed to detect names of people with the structure "Mrs. \[male first name\] \[last name\]," such as "Mrs. Ralph Mayer" or "Mrs. Tomás Rivera." It uses [spaCy](https://spacy.io/) and [gender-guesser](https://pypi.org/project/gender-guesser/). 

This comes out of a practical problem identified in an English-language, U.S.-based library and archives metadata context, in which legacy descriptions are often repurposed for digital collections, and dated descriptions don't always align with current modes of address. [Names are complicated](https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/) and this code makes plenty of assumptions about them that are not universal. The goal is not to strive for perfect accuracy or universality, but to flag potential instances in this context where women were not identified by their own names. By flagging these instances we can focus in on them for human review, revision and further research where needed, in order to more equitably name and represent women in descriptive metadata. 

To view a sample report generated with this code, see [sample_report.csv](https://github.com/ngeraci/mrs_names/blob/master/data/sample_report.csv). The test data in [mrs_text_data.csv](https://github.com/ngeraci/mrs_names/blob/master/data/mrs_test_data.csv) comes from legacy metadata from the [Avery E. Field photographs](https://calisphere.org/collections/92/).

This is a work in progress, written as an exploratory experiment by someone who is primarily a metadata librarian rather than a developer. It was developed in a Python 3.7 environment and should work with other 3.x versions, but hasn't been tested extensively.

## Requirements
* spaCy
* spaCy English model
* gender-guesser

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
