#!/usr/bin/python3
import json
import calendar as cal
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def month_stat(year, month):
    monthstr = f'{month:02d}'
    folder = Path(f'data/{year}/{monthstr}')
    repos = []
    for f in folder.glob('*.json'):
        with open(f, 'r') as fp:
            repos += json.load(fp)
        break
    df = pd.DataFrame(repos)
    s = df[df['language'] != None]['language'].value_counts(normalize=True).head(20).mul(100).round(1)
    s = s.rename(cal.month_name[month])
    print(s)
    s.to_csv(f'stat_{year}-{monthstr}.csv')

    s2 = s.rename({'Jupyter Notebook': "Jupyter\nNotebook"})
    plt.rcParams['font.family'] = 'Noto Sans CJK JP'
    s2.plot(
        kind='bar',
        title=f'{year} {cal.month_name[month]} Top 20 Frequently Used Languages on GitHub',
        xlabel='Language', ylabel='Percentage',
        figsize=(20, 10)
    )
    plt.xticks(rotation=0)
    plt.savefig(f'stat_{year}-{monthstr}.png', bbox_inches='tight')
    plt.clf()
    return s

def main():
    slist = [ month_stat(2022, i) for i in range(1, 12) ]
    df = pd.concat(slist, axis='columns', join='inner').head(10)
    print(df)
    df = df.transpose()
    print(df)
    df.to_csv('stat_2022.csv')
    df.plot(
        title='2022 Frequently Used Languages on GitHub',
        xlabel='Month', ylabel='Percentage',
        xticks=range(11),
        marker=".",
        figsize=(20,12)
    )
    print(plt.xticks())
    plt.xticks(ticks=plt.xticks()[0], labels=cal.month_name[1:12])
    print(plt.xticks())
    plt.savefig('stat_2022.png')
    plt.show()
    plt.clf()

if __name__ == '__main__':
    main()

