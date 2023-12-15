import time
from argparse import ArgumentParser

from unifiedDL import RelationalDatabase2RDF, process_auto_mapped_rdf


def directMappingPerformance():
    file = 'performanceSource2.log'
    with open(file, 'a') as write_obj:
        for i in range(1, 1):
            for expNo in range(21, 70):
                connStr = 'vehchain:Inf0Bey0nd!@192.168.1.136/unifiedDLSource2V' + str(i)
                outputPath = 'rdfMappingOutputRaw.n3'
                rdfBase = '<http://infobeyondtech.com/unifieddl/>'

                start = time.time()
                RelationalDatabase2RDF(connStr, outputPath)
                baseLine = '@base ' + rdfBase + ' .'
                process_auto_mapped_rdf(outputPath, baseLine)
                end = time.time()
                DirectMappingAlgorithmDuration = end - start
                write_obj.write(str(expNo) + ' ' + 'unifiedDLSource2V' + str(i) + ' ' + str(DirectMappingAlgorithmDuration))
                print str(expNo) + ' ' + 'unifiedDLSource2V' + str(i) + ' ' + str(DirectMappingAlgorithmDuration)
                write_obj.write("\n")
                time.sleep(1)
    pass


def directMapping():
    # connStr = 'vehchain:Inf0Bey0nd!@192.168.1.136/unifiedDLSource1V19'
    # connStr = 'vehchain:Inf0Bey0nd!@localhost:3307/unifiedDLSource1V20'
    outputPath = 'rdfMappingOutputRaw.n3'
    rdfBase = '<http://infobeyondtech.com/unifieddl/>'

    parser = ArgumentParser()
    parser.add_argument("-c", type=str, help="database connection string", dest="connStr", required=True)
    args = parser.parse_args()

    if args.connStr:
        connStr = args.connStr


    RelationalDatabase2RDF(connStr, outputPath)
    baseLine = '@base ' + rdfBase + ' .'
    process_auto_mapped_rdf(outputPath, baseLine)


if __name__ == '__main__':
    # directMappingPerformance()
    directMapping()
