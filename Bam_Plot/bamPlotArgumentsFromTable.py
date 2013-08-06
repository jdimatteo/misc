#!/bin/python

import csv
import sys

def isRgbValue(value):
    try:
        return 0 <= int(value) <= 255
    except ValueError:
        return False

if len(sys.argv) != 4:
    print "Usage: %s <table_data_file> <name_selection_from_data_file> <color_override>" % sys.argv[0]
    print ""
    print "Returns the corresponding bam file, genome, and color in the following format: BAM_FILE -g GENOME -c COLOR" 
    print ""
    print "If the color override is not an empty string, then it is used."
    print ""
    print "Examples:"
    print ""
    print '\t$ %s /home/data/MM1S_Table.txt MM1S_BRD4_500nM_JQ1 ""' % sys.argv[0]
    print "\t05242012_D0WUYACXX_3.ACAGTG.hg18.bwt.sorted.bam -g hg18 -c 47,26,251" 
    print "\t$"
    print ""
    print '\t$ %s /home/data/MM1S_Table.txt MM1S_CDK9_500nM_JQ1 "255,132,0"' % sys.argv[0]
    print "\t08282012_C1260ACXX_6.CGTACG.hg18.bwt.sorted.bam -g hg18 -c 255,132,0" 
    print "\t$"
    sys.exit(-1)

(table_data_file_name, name, color_override) = (sys.argv[1], sys.argv[2], sys.argv[3])

# files are assumed to be in a format such as the following:
# NAME    UNIQUE_ID       BAM_FILE        GENOME  COLOR
# MM1S_BRD4_500nM_JQ1     05242012_D0WUYACXX_3.ACAGTG     05242012_D0WUYACXX_3.ACAGTG.hg18.bwt.sorted.bam hg18    47,26,251
name_col   = 0
id_col     = 1
file_col   = 2
genome_col = 3
color_col  = 4

with open(table_data_file_name, 'r') as table_data_file:
    reader = csv.reader(table_data_file, delimiter='\t')
   
    for record in reader:
        if record[name_col] == name:
            if color_override != '':
                try:
                    color = color_override.replace(" ", "") # remove any spaces a user may have erroneously added
                    rgb = color.split(",")
                    
                    # verify that we have three integers between values of 0 and 256
                    if len(rgb) != 3 or not isRgbValue(rgb[0]) or not isRgbValue(rgb[1]) or not isRgbValue(rgb[2]):
                        raise Exception("invalid color: %s" % rgb)
                except:
                    print 'Color "%s" is invalid, defaulting to color in data table' % color_override
                    color = record[color_col]
            else:
                color = record[color_col]

            print "%s -g %s -c %s" % (record[file_col], record[genome_col], color) 
            sys.exit(0)

print "Record not found for name '%s'" % name
sys.exit(1)
