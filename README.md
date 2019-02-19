# mrs

This is an experiment in creating a Python library designed to detect names of people with the structure "Mrs. \[male first name\] \[last name\]," such as "Mrs. Ralph Mayer" or "Mrs. Tomás Rivera." It uses [spaCy](https://spacy.io/) and [gender-guesser](https://pypi.org/project/gender-guesser/). 

It comes out of a library and archives metadata context, where dated descriptions don't always align with current modes of address. The goal is to identify potential instances where women were not identified by their own names, in order to target those instances for revision and further research where needed. 

This is very much a work in progress, written as an exploratory experiment by someone who is primarily a metadata librarian rather than a developer.

## Usage
```python
import mrs

data = mrs.Text(input_string)

# Text.mrs_names is a list of entities from the input text that have been
# identified as personal names preceded by "Mrs"
for entity in data.mrs_names:
    name = mrs.Name(entity)
    # Potential Name.format values are "first_last", "initials", and "surname_only"
    # Only names with format "first_last" have a non-null gender_guess value
    if name.format == "first_last":
    	# Name.text is the name string
    	# Name.gender_guess is the value returned by gender_guesser (unknown (name not found),
            andy (androgynous), male, female, mostly_male, or mostly_female)
    	print(name.text, name.gender_guess)

```
For a complete example of analyzing a tabular metadata file and creating a CSV report, see [example.py](https://github.com/ngeraci/mrs_names/blob/master/example.py).