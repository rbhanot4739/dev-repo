import xml.etree.ElementTree as XP
from memory_profiler import profile


def readXml(FH):
    tree = XP.parse(FH)
    root = tree.getroot()
    # print(root, " ", len(root))  # Length of root element is the number of child elements in it.
    # print(root[4].attrib)  # lists the attributes of the xml element in a dictionary

    # Finding elements
    # print(root.find('book'))  # Returns only the first element matched
    books = root.findall('book')  # Returns a list of all the matching elements

    # Traversing inside the elements
    for book in books:
        print(book.get('id'), end=' - ')  # get method is used to fetch the attribute of a element
        print(book.find('title').text, end=' - ')
        print("INR ", book.find('price').text)


if __name__ == '__main__':
    with open('test.xml', 'rt') as inFile:
        readXml(inFile)
