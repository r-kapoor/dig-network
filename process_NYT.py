from lxml import etree


"/home/rkapoor/Documents/ISI/data/NYT/nyt_corpus/dtd/nitf-3-3.dtd"

tree = etree.parse("/home/rkapoor/Documents/ISI/data/NYT/nyt_corpus/data/1987/01/01/01/0000000.xml")
root = etree.Element("root")

print(etree.tostring(tree))