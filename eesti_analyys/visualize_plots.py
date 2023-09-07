import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def generate_plot(dataset, column_name, nr_of_bins, xlabel, ylabel):
    sns.set(style="whitegrid")
    sns.histplot(data=dataset[column_name], binwidth=nr_of_bins)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.axvline(x=dataset[column_name].mean(), color='red', ls='--', lw=2.5, label=f'{round(dataset[column_name].mean(), 1)} (average)')
    plt.axvline(x=dataset[column_name].median(), color='black', ls='-', lw=2, label=f'{dataset[column_name].median()} (median)')
    plt.axvline(x=dataset[column_name].max(), color='orange', ls='-', lw=2.5, label=f'{round(dataset[column_name].max(), 1)} (max)')
    plt.axvline(x=dataset[column_name].min(), color='orange', ls='--', lw=2.5, label=f'{round(dataset[column_name].min(), 1)} (min)')
    plt.legend(loc=1)
    plt.savefig(f'{column_name}_plot.png')

f = 'limesurvey_stats.csv'
pd_dataset = pd.read_csv(f)
# generate_plot(pd_dataset, 'word_c', 50, 'word count', 'number of texts')
# generate_plot(pd_dataset, 'lemma_c', 25, 'lemma count', 'number of texts')
generate_plot(pd_dataset, 'avg_len', 5, 'average sentence length', 'number of texts')

