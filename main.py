"""
Customer To KML
Assembled by FAV on 08 06 13
Connects to a data source containing addresses,
geocodes the addresses with Google's geocode API, and stores them in KML format.
"""

from controller import Controller
from model import CtkModel as model


def main():
    """Enter the program"""
    ctr = Controller(model())
    ctr.display()
    ctr.end()

if __name__ == "__main__":
    main()
