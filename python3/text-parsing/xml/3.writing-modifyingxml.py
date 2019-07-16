import xml.etree.ElementTree as ET


def write_xml():
    with open('new.xml', 'w') as IF:
        root = ET.Element('root')
        child1 = ET.SubElement(root, 'child1')
        child1.text = 'I am the first child'
        child2 = ET.SubElement(root, 'child2')
        child2.text = 'I am second child'
        grandchild1 = ET.SubElement(child1, 'grandchild1')
        grandchild1.text = 'I am grandchild of root'
        tree = ET.ElementTree(root)
        # ET.dump(root)
        print(ET.tostring(root,
                          encoding='unicode'))  # Used to print string repr of xml element  # tree.write(IF, encoding="unicode")


def mod_xml(IF):
    tree = ET.parse(IF)
    root = tree.getroot()

    # for book in root.findall('book'):
    #     n_price = int(book.find('price').text) + 150
    #     book.find('price').text = str(n_price)
    #

    # Same functionality but using iter() method

    for price in root.iter('price'):
        n_price = int(price.text) + 50
        price.text = str(n_price)
    tree.write('out.xml')


if __name__ == '__main__':
    write_xml()  # with open('test.xml', 'rt') as IF:  #     mod_xml(IF)
