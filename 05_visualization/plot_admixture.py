# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 19:53:53 2017

@author: Caiyd
"""


import json
import click
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns


def load_qopt(qoptfile: str, k: int):
    """
    K是祖先数
    """
    df = pd.read_csv(qoptfile, sep=' ', usecols=list(range(k)), header=None).T
    cols = [f'Ind{i}' for i in range(0, df.shape[1])]
    df.columns = cols
    return df


def load_sminfo(infofile: str):
    """
    indv    IID     GID
    Ind116  IRCA02  IRCA
    Ind119  IRCA05  IRCA
    Ind121  IRCA07  IRCA
    """
    info_df = pd.read_csv(infofile, sep='\t')
    return info_df


def draw(df, info_df: pd.DataFrame, colors: list, outprefix):
    sm_order = info_df['indv'].values.tolist()
    df = df[sm_order]
    indlabels = [info_df.loc[info_df['indv']==x, 'IID'].values[0] for x in df.columns] # 排序后对应的个体ID
    fig, ax = plt.subplots(1, 1, figsize=(40, 10))
    sns.set_style('white')
    ind = np.arange(df.shape[1])
    wd = 1
    bt = [0] * len(ind)
    k = df.shape[0]
    for i in range(0, k):
        ax.bar(left=ind, height=df.iloc[i, :].values, width=wd, bottom=bt, color=colors[i])
        bt = df.iloc[i, :].values + bt
    ax.set_xlim(-0.5, len(ind)-0.5)
    ax.set_xticks(ind)
    ax.set_xticklabels(indlabels, rotation='vertical')
    ax.yaxis.set_visible(False)
    plt.savefig(f'{outprefix}.pdf')
    plt.savefig(f'{outprefix}.jpg', dpi=300)



@click.command()
@click.option('--indir', help='包含admixture结果文件的目录, 默认当前目录', default='.')
@click.option('--infofile', help='样本信息，indv\\tIID\\tGID三列,indv从Ind0开始,有header, 可以排好序')
@click.option('--colorfile', help='颜色配置，一行一个RGB值(16进制)')
@click.option('--outprefix', help='输出文件前缀')
def main(indir, infofile, colorfile, outprefix):
    info_df = load_sminfo(infofile)
    with open(colorfile) as f:
        colors = json.load(f)
    for file in Path(indir).glob('*.*.Q'):
        k = file.name.split('.')[-2]
        if k.isdigit():
            df = load_qopt(file, int(k))
            draw(df, info_df, colors[k], f'{outprefix}.{k}')

if __name__ == '__main__':
    main()
