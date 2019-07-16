import xml.etree.ElementTree as XP


def Main():
    tree = XP.parse('reed.xml')
    root = tree.getroot()

    print('--------- Demonstrating Iter and Iterfind ---------')
    # for elem in root.iter():  # To iter through all the elements starting from root element
    #     print(elem.tag)

    # for elem in root.iter('title'):  # To iter through all the 'title' tag elements starting from root element
    #     print(elem)

    # for elem in root.itertext():
    #     print(elem)

    for title in root.findall('.//title'):  # using `.//` in findall it will search the entire tree otherwise find will
        # search only in direct children
        print(title)


if __name__ == '__main__':
    Main()
