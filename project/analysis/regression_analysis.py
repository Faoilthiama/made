import pandas as pd
import statsmodels.api as sm
from matplotlib import pyplot as plt

from project.analysis import common


def linear_regression():
    life_expectancy, health_expenditure = common.load_datasets()

    health_expenditure_long = pd.melt(health_expenditure, id_vars=['Country Code', 'Country Name'], var_name='Year',
                                      value_name='Health_Expenditure')
    life_expectancy_long = pd.melt(life_expectancy, id_vars=['Country Code', 'Country Name'], var_name='Year',
                                   value_name='Life_Expectancy')
    data = pd.merge(health_expenditure_long, life_expectancy_long, on=['Country Code', 'Country Name', 'Year'])

    X = data[['Health_Expenditure']]  # Independent variable (Health Expenditure)
    Y = data['Life_Expectancy']

    X_with_const = sm.add_constant(X)

    model = sm.OLS(Y, X_with_const)
    model = model.fit()

    print(model.summary())

    Y_pred = model.predict(X_with_const)

    plt.figure(figsize=(10, 6))

    plt.scatter(X, Y, color='blue', label='Actual Data')
    plt.plot(X, Y_pred, color='red', linewidth=2, label='Regression Line')

    plt.title('Linear Regression: Health Expenditure vs Life Expectancy')
    plt.xlabel('Health Expenditure')
    plt.ylabel('Life Expectancy')

    plt.legend()
    plt.savefig('regression.png')
    plt.show()
    plt.close()


if __name__ == "__main__":
    # subprocess.call("./pipeline.sh")
    linear_regression()
