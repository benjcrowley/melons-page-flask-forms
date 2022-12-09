import csv
from pprint import pprint

melons_list = []
melons_dictionary = {}

class Melon:
    """
    A melon in a melon type

    Attributes melon_id, common_name, price, image_url, color, seedless
    return: a Melon object
    """

    def __init__(
        self,
        melon_id,
        common_name: str,
        price: float,
        image_url: str,
        color: str,
        seedless: bool,
    ):
        self.melon_id = melon_id
        self.common_name = common_name
        self.price = price
        self.image_url = image_url
        self.color = color
        self.seedless = seedless

    def __str__(self) -> str:
        """Convient method to display melons"""
        return f"{self.common_name},{self.price},{self.color},{self.seedless},{self.image_url}"

    def __repr__(self) -> str:
        """Convient method to display melons"""
        return f"<melon : {self.melon_id}: {self.common_name}"

    def price_str(self):
        """return price in string format $x.xx"""
        return f"${self.price:.2f}"



with open("melons.csv", "r") as file:
    reader = csv.DictReader(file)

    for line in reader:
        # print(line['melon_id'])
        melon = Melon(
            line["melon_id"],
            line["common_name"],
            float(line["price"]),
            line["image_url"],
            line["color"],
            eval(line["seedless"]),
        )
        # melons_list.append(melon)
        melons_dictionary[melon.melon_id] = melon


def get_by_id(melon_id):
    """
    Given a melon ID, return a Melon object from the dictionary

    ;param melon_id: a four letter code to id a melon. string
    ;return: a Melon object
    """
    if melon_id in melons_dictionary:
        return melons_dictionary[melon_id]
    else:
        return None
    # A function to look up a Melon object given its melon_id and return the object. If the melon_id is not found, return None.


# A function to get a list of the Melon objects (which are all values in our melon_dict) and return the list.
def get_all():
    """A function to return a list of all the melons in the dictionary"""
    return list(melons_dictionary.values())


# A function to remove a melon from the dictionary given its melon_id. If the melon_id is not found, return None.
def remove_by_id(melon_id):
    """
    A function to remove a melon from the dictionary given its melon_id. If the melon_id is not found, return None.

    ;param melon_id: a four letter code to id a melon. string
    ;return: True if melon is removed, False if melon is not found
    """
    if melon_id in melons_dictionary:
        melons_dictionary.pop(melon_id)
        return True
    else:
        return False


# test code

# print(get_by_id("cong"))
# pprint(get_all())
# print(remove_by_id("wils"))
# pprint(get_all())
# print(melons_dictionary["cong"].price_str())
# print(melons_dictionary["cong"].hello())
# pprint(melons_dictionary)
