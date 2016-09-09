import xml.etree.ElementTree as ETree
from chromosome import Chromosome
import re
import sqlite3


sql = sqlite3.connect('simulation_db.sqlite').cursor()

chromosome = Chromosome("c_test1", [20000], [], 65000, 50, 10)
tree = ETree.parse()
root = tree.getroot()
for child in root[0]:
    region_string = child[1].text.replace(',', '')
    direction = re.search('[(](.)[)]', region_string).group(0)
    transcription_start = int(re.search('(?<=:\s)\d+', region_string).group(0))
    transcription_end = int(re.search('(?<=-\s)\d+', region_string).group(0))
    if direction == "(-)":
        transcription_start, transcription_end = transcription_end, transcription_start

    chromosome.add_transcription_region(transcription_start, transcription_end, 30, 20)

print(chromosome)
