import sys
import csv

try:
    csv_first_names = open("C:\\Users\\Dmitry\\Desktop\\names.csv", "r")
except IOError:
    print "Error: No CSV First Names file was found"
    sys.exit(1)

universal_first_names = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [],
    'h': [], 'i': [], 'j': [], 'k': [], 'l': [], 'm': [], 'n': [],
    'o': [], 'p': [], 'q': [], 'r': [], 's': [], 't': [], 'u': [],
    'v': [], 'w': [], 'x': [], 'y': [], 'z': []}

"""
    First extract relevant names from csv files,
    which we assume our given names exist in.
"""
first_name_list = []
reader = csv.reader(csv_first_names)
for line in reader:
    first_name_list.append(line)

for names_group in first_name_list:
    universal_first_names[names_group[0][0]].append(list(names_group))


class person():
    @staticmethod
    def match_related_names(names):
        """
        That is, for each name in the first name (including middle names),
        we create a set of related names, and store them in list (of sets).
        """
        l = []
        for person_name in names:
            # Most people have either one or two names (middle names).
            # Still exceptions exist like - John Felix Anthony .

            if len(person_name) > 1:
                # Marking name as single letter does not provide us enough information about the personality.
                s = set()
                for group in universal_first_names[person_name[0].lower()]:
                    if person_name.lower() in group:
                        for related_name in group:
                            s.add(related_name)
                l.append(s)
        return l

    @staticmethod
    def is_first_name(name):
        for group in first_name_list:
            if name.lower() in group:
                return True

        return False

    @staticmethod
    def equal_last_names(ln1, ln2):
        if ln1.lower() == ln2.lower():  # That is obvious ...
            return True

        if len(ln1) == len(ln2):
            # Maybe few letters were misspelled
            if ln1[0] == ln2[0]:
                unequal_chars_indexes = [index for index, letter in enumerate(ln1) if letter != ln2[index]]
                if len(unequal_chars_indexes) == 1:
                    # Apparently small misspell, we will forgive the typist ...
                    return True
                elif len(unequal_chars_indexes) == 2:
                    # We will set two characters as limit
                    if len(ln1) == 3 or len(ln1) == 4:
                        # The Names are too short to be misspelled that relatively badly
                        return False

                    vowels = ('a', 'e', 'i', 'o', 'u')
                    """consonants = ('b', 'c', 'd', 'f', 'g', 'h', 'j',
                                  'k', 'l', 'm', 'n', 'p', 'q', 'r',
                                  's', 't', 'v', 'w', 'x', 'y', 'z')"""

                    """
                    It is intuitive that if the names are meant to be equal, then one of the following is possible :
                        - Both of the unequal characters are consonants
                        - One character is vowel and the second one is consonant

                    Otherwise the names are spelled differently one from another,
                    and therefore are unequal.
                    """
                    return bool(not(ln1[unequal_chars_indexes[0]] in vowels and ln1[unequal_chars_indexes[1]] in vowels
                                    and ln2[unequal_chars_indexes[0]] in vowels and ln2[unequal_chars_indexes[1]] in vowels))

                else:
                    # Most chances the names are different
                    return False
            else:
                """
                It is really unlikely for the same person to misspell the first letter
                of his last name.
                """
                return False

        else:   # Apparently not equal
            if ln1.lower() in ln2.lower() or ln2.lower() in ln1.lower():
                # A very very simple sanity check
                return True
            else:
                return False

    @classmethod
    def analyze_name_on_bill(cls, parts):
        """
        As the nature of names on bill, they tend to have various types
        and combinations, i.e:
            - Egli Deborah
            - Deborah Egli

        So we ought to scan through each part of the name to determine its nature.
        """
        if len(parts) == 2:
            # We assume that if a name/part does not exit in the
            # name/nickname data base (csv file), then it should be family name,
            # as it can take any form.

            # We check always the first name out of a group of names
            if person.is_first_name(parts[0]):
                return cls(parts[0].split(), parts[1])
            elif person.is_first_name(parts[1]):
                return cls(parts[1].split(), parts[0])
        else:
            print "Error: Bill name on card must have the form - [Official First Name] [Official Last Name]."
            sys.exit(3)

    def get_names_sets(self):
        return self.possible_first_names

    def get_last_name(self):
        return self.last_name

    def __init__(self, first_name, last_name):
        self.possible_first_names = person.match_related_names(first_name)
        """
        Well, unlike first names, which can have various combinations, nicks
        (i.e Deb = Debbi = Debbie = Debbra = Debby = Deborah...), last names tend to be constant.
        Hence, a any variation we expect will take form of minor letter change,
        uppercase/lowercase and so on like Hodgen = Hodgens = Hodges
        """
        self.last_name = last_name


def are_the_same_people(p1, p2):
    if person.equal_last_names(p1.get_last_name(), p2.get_last_name()):
        # If last name don't match, it is clear we have different people
        p1_names_sets = p1.get_names_sets()
        p2_names_sets = p2.get_names_sets()

        if len(p1_names_sets) == len(p2_names_sets):
            # If we have the same number of first & middle names,
            # they should correlate to each other.
            for i in range(0, len(p1_names_sets)):
                if not (p1_names_sets[i] & p2_names_sets[i]):
                    return False
            return True
        else:
            # Otherwise, we are interested in the first first name
            return bool(p1_names_sets[0] & p2_names_sets[0])
    else:
        return False


def countUniqueNames(billFirstName, billLastName,
                     shipFirstName, shipLastName,
                     billNameOnCard):

    if not billFirstName or not billLastName or not shipFirstName or not shipLastName or not billNameOnCard:
        print "Error: Missing information"
        sys.exit(2)

    p1 = person(billFirstName.split(), billLastName)
    p2 = person(shipFirstName.split(), shipLastName)
    p3 = person.analyze_name_on_bill(billNameOnCard.split())

    # Compare the profiles
    first_is_second = are_the_same_people(p1, p2)
    first_is_third = are_the_same_people(p1, p3)
    second_is_third = are_the_same_people(p2, p3)

    # And now to the last (and simple) logic :
    if first_is_second:
        if first_is_third:
            return 1
        else:
            return 2
    else:
        if first_is_third:
            return 2

        if second_is_third:
            return 2
        else:
            return 3

if __name__ == "__main__":

    # The original unit tests
    print countUniqueNames("Deborah", "Egli", "Deborah", "Egli", "Deborah Egli")
    print countUniqueNames("Deborah", "Egli", "Debbie", "Egli", "Debbie Egli")
    print countUniqueNames("Deborah", "Egni", "Deborah", "Egli", "Deborah Egli")
    print countUniqueNames("Deborah S", "Egli", "Deborah", "Egli", "Egli Deborah")
    print countUniqueNames("Michelle", "Egli", "Deborah", "Egli", "Michelle Egli")

    # Mine additional ones ...
    # 1) Do this and the program will exit with code : 2 - print countUniqueNames("", "Egli", "Deborah", "Egli", "Michelle Egli")

    # 2) Three persons - Prints 3
    print countUniqueNames("Deborah", "Egli", "Al", "Eglias", "Michelle Egli")

    # 3) Last name misspelling - 2 letters : Prints 1, as it accounts for occasional misspelling
    print countUniqueNames("Albert", "Einstein", "Albert", "Eimsteim", "Albert Einstein")

    # 4) Secondary names examples - 2 equal first names: Prints 1
    print countUniqueNames("Deb Michelle", "Egli", "Debby Michelle", "Egli", "Debby Egli")

    # 5) Secondary names examples - 3 first names VS 1 first name:
    # Prints 1, as it assumes that only the first name matters in such cases.
    print countUniqueNames("John Felix Abraham", "Cena", "John", "cena", "John Cena")

    # 5) Unlike the previous example (4), both of the first first names are equal,
    # but the second first name is not (Phillip != Gilbert). Hence, it is logical to
    # assume that people whose second given at birth differs (despite having the same first first name),
    # are not the same guy.
    # Prints 2.
    print countUniqueNames("Harry Phillip", "Williams", "Harry Gilbert", "Williams", "Harry Williams")

    csv_first_names.close()
