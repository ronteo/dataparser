import argparse
from datetime import datetime, date
import os

import pandas as pd

EXPECTED_HEADER = """"Date", "Time", "O", "H", "L", "C", "U"
"""
PRICE_COLUMNS = ["O", "H", "L", "C"]
INPUT_FOLDER = "input"

def fix_precision(s):
    return "%.2f" % float(s)

def main():

    for dir in os.listdir(INPUT_FOLDER):
        df = pd.DataFrame()
        for f in os.listdir(os.path.join(INPUT_FOLDER, dir)):
            filename = os.path.join(INPUT_FOLDER, dir, f)
            header = None
            for l in open(filename):
                header = l
                header = [h.replace("\"", "").strip() for h in header.split(",")]
                break
            df = df.append(pd.read_csv(filename, dtype={"Time": str}, names=header, skiprows=1))

        print(df.columns)
        for c in PRICE_COLUMNS:
            df[c] = df.apply(lambda x: fix_precision(x[c]), axis=1)
        df["Time"] = df.Time.apply(lambda x: str(x)[:4])
        df["DateTimeTypeCol"] = df.apply(lambda x: datetime.strptime(str(x.Date) + x.Time, '%Y%m%d%H%M'), axis=1)
        df.sort_values(by=["DateTimeTypeCol"], inplace=True)
        df.drop_duplicates(subset=["Date", "Time"], inplace=True)
        del df['DateTimeTypeCol']
        output_file = os.path.join("output", dir, str(date.today()) + ".txt")

        out_folder = os.path.split(output_file)[0]
        if(not os.path.exists(out_folder)):
            os.mkdir(out_folder)


        df.to_csv(output_file, index=False)
        print("Output written to: %s" % output_file)

if __name__ == "__main__":
    main()
