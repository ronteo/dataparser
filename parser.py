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

def main():

    for dir in os.listdir(INPUT_FOLDER):
        df = pd.DataFrame()
        for f in os.listdir(os.path.join(INPUT_FOLDER, dir)):
            df = df.append(pd.read_csv(os.path.join(INPUT_FOLDER, dir, f)))

        df.columns = [c.replace("\"", "").strip() for c in df.columns]

        print(df.columns)
        for c in PRICE_COLUMNS:
            df[c] = df.apply(lambda x: fix_precision(x[c]), axis=1)
        df['DateTypeCol'] = pd.to_datetime(df.Date)
        df["Time"] = df.Time.apply(lambda x: int(str(x)[:4]))
        df.sort_values(by=["DateTypeCol", "Time"], inplace=True)
        df.drop_duplicates(subset=["Date", "Time"], inplace=True)
        del df['DateTypeCol']
        output_file = os.path.join("output", dir, str(date.today()) + ".txt")
        
        out_folder = os.path.split(output_file)[0]
        if(not os.path.exists(out_folder)):
            os.mkdir(out_folder)
        

        df.to_csv(output_file, index=False)
        print("Output written to: %s" % output_file)

if __name__ == "__main__":
    main()
