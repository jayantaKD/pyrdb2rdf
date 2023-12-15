from argparse import ArgumentParser

from unifiedDL import process_auto_mapped_rdf, JSONDatabase2RDF

if __name__ == '__main__':
    connStr = 'vehchain:Inf0Bey0nd!@192.168.1.136/unifiedDLSource1V3'
    outputPath = 'rdfMappingOutput.n3'
    rdfBase = '<http://infobeyondtech.com/unifieddl/>'

    parser = ArgumentParser()
    parser.add_argument("-c", type=str, help="database connection string", dest="connStr", required=True)
    args = parser.parse_args()

    if args.connStr:
        connStr = args.connStr

    JSONDatabase2RDF()
    baseLine = '@base ' + rdfBase + ' .'
    process_auto_mapped_rdf(outputPath, baseLine)