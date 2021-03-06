import operator

PEOPLE = [
    ("Donald", "Trump", 7.85),
    ("Vladimir", "Putin", 3.626),
    ("Jinping", "Xi", 10.603),
]


def format_sort_records(list_of_tuples):
    output = []
    template = "{1:10} {0:10} {2:5.2f}"
    for person in sorted(list_of_tuples, key=operator.itemgetter(1, 0)):
        output.append(template.format(*person))
    return output


print("\n".join(format_sort_records(PEOPLE)))

"""
If you find tuples annoying because they use numeric indexes, you’re not alone!
Reimplement this exercise using namedtuple objects (http://mng.bz/gyWl),
defined in the collections module. Many people like to use named tuples
because they give the right balance between readability and efficiency.
"""


"""
Define a list of tuples, in which each tuple contains the name, length (in min-
utes), and director of the movies nominated for best picture Oscar awards last
year. Ask the user whether they want to sort the list by title, length, or director’s
name, and then present the list sorted by the user’s choice of axis.
"""

"""
Extend this exercise by allowing the user to sort by two or three of these fields,
not just one of them. The user can specify the fields by entering them separated
by commas; you can use str.split to turn them into a list.
"""
