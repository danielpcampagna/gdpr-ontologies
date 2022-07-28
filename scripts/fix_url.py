import csv, os, shutil

def fix_url(input: str, mapper: str, output: str, **args):

    delimiter = args.pop("delimiter", ",")
    quotechar = args.pop("quotechar", "|")

    if len(args) > 0:
        raise f"Extra parameters {args.keys()}"

    tmpfile = f'{output}.tmp'
    shutil.copyfile(input, tmpfile)

    with open(mapper, 'r') as mf:
        mfreader = csv.reader(mf, delimiter=delimiter, quotechar=quotechar)
        for row in mfreader:
            src, dst = row
            with open(tmpfile, 'r') as inf:
                with open(output, 'w') as outf:
                    outf.writelines([inline.replace(src, dst) for inline in inf.readlines()])
            shutil.copyfile(output, tmpfile)
        os.remove(tmpfile)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Fix ontology concepts url.')
    parser.add_argument(dest='input', help='input ontology file (e.g., "onto.owl")')
    parser.add_argument('-m', dest='mapper', help='map file, a csv-like containg the source and the final name (e.g., "map.csv").')
    parser.add_argument('-o', dest='output', help='The output file with new urls.')
    
    parser.add_argument('--delimiter', default=",", dest='delimiter', help='The delimiter used in the map file. (default: ","')
    parser.add_argument('--quotechar', default=",", dest='quotechar', help='The quotechar used in the map file. (default: "|"')

    args = parser.parse_args()
    # print()
    fix_url(**args.__dict__)