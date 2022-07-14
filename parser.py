import argparse
from datetime import date

EXPECTED_HEADER = """"Date", "Time", "O", "H", "L", "C", "U"
"""

def fix_precision(s):
    return "%.2f" % float(s)

def main(*argv):
    header_written = False
    output_file = "output_%s.txt" % date.today()
    with open(output_file, "w+") as f:
        for arg in argv:
            print("Processing file:%s" % arg)
            for i, line in enumerate(open(arg)):
                if i == 0:
                    assert line == EXPECTED_HEADER, "Error! Columns should be:\n%s\bFound:\n%s" % (EXPECTED_HEADER, line)
                    if not header_written:
                        f.write(line)
                        header_written = True
                else:
                    arr = line.split(",")
                    for i in range(2, 6):
                        arr[i] = fix_precision(arr[i])
                    f.write(",".join(arr))
    print("Output written to: %s" % output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process market data.')
    parser.add_argument('files', metavar='f', type=str, nargs='+',
                        help='path to files. files will be cleaned and appended in order to a single file')
    args = parser.parse_args()
    main(*args.files)
