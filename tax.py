import pandas as pd
import csv
import logging


LOG: logging.Logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    w2_1 = pd.read_csv('input/w2_1.csv')
    w2_2 = pd.read_csv('input/w2_2.csv')
    f1040 = {}
    f1040['1a'] = w2_1.iloc[0]['box1'] + w2_2.iloc[0]['box1']
    f1040['1b'] = 0
    f1040['1c'] = 0
    f1040['1d'] = 0
    f1040['1e'] = 0
    f1040['1f'] = 0
    f1040['1g'] = 0
    f1040['1h'] = 0
    f1040['1i'] = 0
    f1040['1z'] = f1040['1a'] + f1040['1b'] + f1040['1c'] + f1040['1d'] + f1040['1e'] + f1040['1f'] + f1040['1g'] + f1040['1h']

    f1040['2a'] = 0  # Tax-Exempt Interest

    f1099int = pd.read_csv('input/1099-INT.csv')
    f1099div = pd.read_csv('input/1099-DIV.csv')
    f1040sb = {}
    f1040sb[2] = f1099int.box1.sum()
    f1040sb[3] = 0  # Excludable interest on series EE and I U.S. savings bonds issued after 1989
    f1040sb[4] = f1040sb[2] - f1040sb[3]
    f1040['2b'] = f1040sb[4]  # Taxable Interest
    must_complete_1040sb_part3 = f1040sb[4] > 1500


    LOG.info("Generating F1040 Schedule B...")
    f1040sb_file = 'output/f1040sb.csv'
    with open(f1040sb_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["1", ""])
        f1099int.to_csv(file, mode="w+", index=False, header=False)
        for k, v in f1040sb.items():
            writer.writerow([k, v])
        # Part II
        writer.writerow([5, ""])
        f1099div.to_csv(file, mode="w+", index=False, header=False)

    f1040sb2 = {}  # Second half of F1040 SB. Two parts to cope with multi-line boxes above.
    f1040['3a'] = 0  # Qualified dividends
    f1040sb2[6] = f1099div.amount.sum()
    f1040["3b"] = f1040sb2[6]  # Ordinary dividends
    if f1040sb2[6] > 1500:
        must_complete_1040sb_part3 = True
    if must_complete_1040sb_part3:
        LOG.info("Must complete F1040 Schedule B Part III.")
    # Part III
    f1040sb2["7a"] = [True, True]
    f1040sb2["7b"] = "China"
    f1040sb2["8"] = False  # foreign trust
    with open(f1040sb_file, 'a', newline='') as file:
        writer = csv.writer(file)
        for k, v in f1040sb2.items():
            writer.writerow([k, v])

    f1040['4a'] = f1040["4b"] = 0
    f1040['5a'] = 0
    f1040['5b'] = 0
    f1040['6a'] = 0
    f1040['6b'] = 0
    f1040['6c'] = 0
    f1040['7'] = 0
    # schedule1  line10
    f1040['8'] = 0

    f1040['9'] = f1040['1z'] + f1040['2b'] + f1040['3b'] + f1040['4b'] + f1040['5b'] + f1040['6b'] + f1040['7'] + f1040['8']
    # schedule1  line26
    f1040['10'] = 0
    f1040['11'] = f1040['9'] - f1040['10']
    f1040['12'] = 200
    f1040['13'] = 0
    f1040['14'] = f1040['12'] + f1040['13']
    f1040['15'] = f1040['14'] + f1040['11']

    f1040['16'] = 0
    # Schedule 2, line 3
    f1040['17'] = 0
    f1040['18'] = f1040['16'] + f1040['17']
    f1040['19'] = 0
    # Schedule 3, line 8
    f1040['20'] = 0
    f1040['21'] = f1040['19'] + f1040['20']
    f1040['22'] = f1040['21'] - f1040['18']
    if f1040['22'] < 0:
        f1040['22'] = 0
    # Schedule 2, line 21
    f1040['23'] = 0
    f1040['24'] = f1040['22'] + f1040['23']

    f1040['25a'] = w2_1.iloc[0]['box2'] + w2_2.iloc[0]['box2']
    # 1099-R box4
    f1040['25b'] = 0
    # W-2G box4
    f1040['25c'] = 0
    f1040['25d'] = f1040['25a'] + f1040['25b'] + f1040['25c']
    f1040['26'] = 0
    f1040['27'] = 0
    f1040['28'] = 0
    f1040['29'] = 0
    f1040['30'] = 0
    f1040['31'] = 0
    f1040['32'] = 0
    f1040['33'] = f1040['25d'] + f1040['26'] + f1040['32']
    if f1040['33'] > f1040['24']:
        f1040['34'] = f1040['33'] - f1040['24']
    else:
        f1040['34'] = 0
    f1040['35a'] = f1040['34']
    f1040['36'] = 0
    f1040['37'] = f1040['24'] - f1040['33']

    LOG.info("Generating F1040...")
    with open('output/f1040.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for k, v in f1040.items():
            writer.writerow([k, v])


if __name__ == "__main__":
    main()
