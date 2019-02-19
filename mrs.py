""" Text analysis library that uses Spacy and gender-guesser
    to identify personal names with the format "Mrs. [male first
    name] [last name].

    This is designed for working with legacy descriptive metadata
    in a library/archives context. The goal is to identify potential
    instances where women were not identified by their own names, in
    order to target those instances for revision.
"""

import re
import spacy
import gender_guesser.detector as gender

GUESSER = gender.Detector()

class Text():
    """ The text object is the body of text being analyzed,
        initialized with a string.
    """

    def __init__(self, input_string):
        self.text = input_string
        self.nlp = spacy.load("en_core_web_sm")
        self.spacy_doc = self.nlp(self.text)
        self.name_entities = self.get_personal_names()
        self.mrs_names = self.get_mrs_names()

    def get_personal_names(self):
        """ Use Spacy named entity recognition to return list
            of entities in the text with type "person"
        """
        personal_names = [
            ent for ent in self.spacy_doc.ents if ent.label_ == "PERSON"
        ]
        return personal_names

    def get_mrs_names(self):
        """ Return list with the text of personal name entities
            whose preceding word matches a regex for "Mrs."
        """
        mrs_names = []
        mrs_regex = re.compile(r"[Mm]rs\.?")
        for name in self.name_entities:
            preceding_word = self.spacy_doc[name.start - 1]
            if re.match(mrs_regex, preceding_word.text):
                mrs_names.append(name.text.strip().replace("\n", " "))
        return mrs_names


class Name():
    """ Name object represents a single name.
    """
    def __init__(self, text):
        self.text = text
        self.format = self.get_name_format()
        self.forename = self.get_forename()
        self.gender_guess = self.forename_gender()

    def get_name_format(self):
        """ Evaluate name string,
            return "surname_only", "initials", or "first_last"
        """

        def single_name(text):
            """ Return True if name contains no spaces.
            """
            # i'm sure there's a more sophisticated way to do this

            return bool(not " " in text)

        def initials_as_first_name(text):
            """ Return True if name matches a regex
                designed for initial-style names (like JD Sampson,
                J. D. Salinger, W.E.B. Du Bois)
            """

            initials_re = re.compile(r"([A-Z][\. A-Z]{1,}){1,} [\w\-']+")
            return bool(re.match(initials_re, text))

        if single_name(self.text):
            name_format = "surname_only"
        elif initials_as_first_name(self.text):
            name_format = "initials"
        else:
            name_format = "first_last"
        return name_format

    def get_forename(self):
        """ If format is first_last, split name text on space and return first component.
            Otherwise, return None.
        """
        if self.format == "first_last":
            forename = self.text.split(" ")[0]
        else:
            forename = None
        return forename

    def forename_gender(self):
        """ If name has a forename, use gender-guesser package to return a guess as to
            the forename's gender. Possible values are unknown (name not found),
            andy (androgynous), male, female, mostly_male, or mostly_female.

            If no forename, return None.
        """
        if self.forename:
            guess = GUESSER.get_gender(self.forename)
        else:
            guess = None
        return guess
