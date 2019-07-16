import xml.etree.ElementTree as ET
from memory_profiler import profile


@profile
def iterparsing():
    print('Parsed with Iterparse !! ')
    for event, elem in ET.iterparse('nasa.xml', events=['start']):
        if event == 'start' and elem.tag == 'title':
            pass  # print(event, " -> ", elem.text)

        #  The call to elem.clear() is key here - iterparse still builds a tree,\
        # doing it on the fly. Clearing the element effectively discards the tree, freeing the allocated memory.
        elem.clear()


@profile
def normal_parsing():
    print('Normal Parsing !!')
    tree = ET.parse('nasa.xml')
    root = tree.getroot()

    for elem in root.iter('title'):
        pass  # print(elem.text)


if __name__ == '__main__':
    iterparsing()
    normal_parsing()
