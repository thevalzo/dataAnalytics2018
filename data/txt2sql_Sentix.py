#
# If you wanto to use on another dictionary, change AFINN-###
#

# retrive all the data
sentix_file = "sentix.txt"
#sentix = dict(map(lambda (k,v): (k,int(v)), [ line.split('\t') for line in open(dictionary_file) ]))

# add the creation table at start
f = open('SENTIX.sql', 'a', encoding='utf-8')
table_creation = """USE data_analytics;
CREATE TABLE `data_analytics`.`sentix` (
  `token` VARCHAR(255) NOT NULL,
  `pos_tag` VARCHAR(45) NULL,
  `wordnet_synset_ID` VARCHAR(45) NULL,
  `positive_score` DECIMAL(14,12) NULL,
  `negative_score` DECIMAL(14,12) NULL,
  `polarity` DECIMAL(14,12) NULL,
  `intensity` DECIMAL(14,12) NULL,
  PRIMARY KEY (`token`, `wordnet_synset_ID`));
"""
f.write(table_creation)
f.close

for line in open(sentix_file, encoding='utf-8'):
    line = line.replace("\r", "")
    line = line.replace("\n", "")
    line = line.split("\t")
    f = open('sentix.sql', 'a', encoding='utf-8')
    f.write("INSERT INTO sentix values(\'"+str(line[0]).replace("'", "\\'")+"\', \'"+str(line[1])+"\', \'"+str(line[2])+"\', \'"+str(line[3])+"\', \'"+str(line[4])+"\', \'"+str(line[5])+"\', \'"+str(line[6])+"\') on duplicate key UPDATE positive_score=\'"+str(line[3])+"\';\n")


f.close()
