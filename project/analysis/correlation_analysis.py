from scipy.stats import pearsonr

from project.analysis import common

ALPHA = 0.05


def correlation_analysis():
    life_expectancy, health_expenditure = common.load_datasets()
    columns = [str(x) for x in range(2000, 2022)]

    correlations = [
        row_correlation(row1, row2)
        for (_, row1), (_, row2) in zip(life_expectancy[columns].iterrows(), health_expenditure[columns].iterrows())
    ]

    # count statistically significant positive and negative samples
    counter_pos = 0
    counter_neg = 0
    counter_zero = 0
    sum_corr_pos = 0
    sum_corr = 0
    for corr, pvalue in correlations:
        if pvalue <= ALPHA:
            if corr > 0:
                counter_pos += 1
                sum_corr_pos += corr
            elif corr < 0:
                counter_neg += 1
                print(corr)
            else:
                counter_zero += 1
            sum_corr += corr

    mean_corr_pos = sum_corr_pos / counter_pos
    mean_corr = sum_corr / len(correlations)
    print(f'{counter_pos=}, {counter_neg=}, {counter_zero=}, {mean_corr_pos=}, {mean_corr=}')


def row_correlation(row1, row2):
    corr, pvalue = pearsonr(row1, row2)
    return corr, pvalue


if __name__ == "__main__":
    # subprocess.call("./pipeline.sh")
    correlation_analysis()
