import argparse
from datetime import date
import os

import pandas as pd

EXPECTED_HEADER = """"Date", "Time", "O", "H", "L", "C", "U"
"""
PRICE_COLUMNS = ["O", "H", "L", "C"]
INPUT_FOLDER = "input"

def fix_precision(s):
    return "%.2f" % float(s)

# def main_old(*argv):
#     header_written = False
#     output_file = "output/%s.txt" % date.today()
#     with open(output_file, "w+") as f:
#         for arg in argv:
#             print("Processing file:%s" % arg)
#             for i, line in enumerate(open(arg)):
#                 if i == 0:
#                     assert line == EXPECTED_HEADER, "Error! Columns should be:\n%s\bFound:\n%s" % (EXPECTED_HEADER, line)
#                     if not header_written:
#                         f.write(line)
#                         header_written = True
#                 else:
#                     arr = line.split(",")
#                     for i in range(2, 6):
#                         arr[i] = fix_precision(arr[i])
#                     f.write(",".join(arr))
#     print("Output written to: %s" % output_file)

def main():
    df = pd.DataFrame()

    for f in os.listdir(INPUT_FOLDER):
        df = df.append(pd.read_csv(os.path.join(INPUT_FOLDER,f)))

    df.columns = [c.replace("\"","").strip() for c in df.columns]

    print(df.columns)
    for c in PRICE_COLUMNS:
        df[c] = df.apply(lambda x: fix_precision(x[c]), axis=1)
    df['DateTypeCol'] = pd.to_datetime(df.Date)
    df.sort_values(by=["DateTypeCol", "Time"], inplace=True)
    del df['DateTypeCol']
    output_file = "output/%s.txt" % date.today()

    df.to_csv(output_file, index=False)
    print("Output written to: %s" % output_file)
if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Process market data.')
    # parser.add_argument('files', metavar='f', type=str, nargs='+',
    #                     help='path to files. files will be cleaned and appended in order to a single file')
    # args = parser.parse_args()
    main()
