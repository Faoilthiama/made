# Project Plan

## Title
Funding Health, Extending Life

## Main Question

*Do higher health expenses per capita increase the life expectancy at birth in Latin American and Caribbean countries?*

## Description

The life expectancy at birth in the LAC region (Latin America and the Caribbean) has continuously changed in the last few years. This project analyzes the influence on health care expenses on the life expectancy in the LAC region, specifically if higher expenses lead to a higher life expectancy. To explore this topic, a data analysis is performed using two data sets. Specifically, the correlation between the two data sets will be explored. The results will give insight into the need for higher healthcare expenses to prolong life.


## Datasources

### Datasource1: Life expectancy at birth, total (years) - Latin America & Caribbean
* Metadata URL: https://data.worldbank.org/indicator/SP.DYN.LE00.IN?locations=ZJ
* Data URL:  https://api.worldbank.org/v2/en/indicator/SP.DYN.LE00.IN?downloadformat=excel
* Data Type: EXCEL

The data set contains data from 1960-2022 so there is quite a lot data available for analysis. Additionally to countries in the LAC region, the data set contains data for countries in other regions like Europe. To perform a successful analysis for the LAC region, these other countries need to be filtered out by using the provided additional Sheet containing country meta data like the region. The data is openly available under the CC BY-4.0 license.

### Datasource2: Current health expenditure per capita, PPP (current international $) - Latin America & Caribbean
* Metadata URL: https://data.worldbank.org/indicator/SH.XPD.CHEX.PP.CD?locations=ZJ
* Data URL: https://api.worldbank.org/v2/en/indicator/SH.XPD.CHEX.PP.CD?downloadformat=excel
* Data Type: EXCEL

The data set contains data from 2000-2021. Additionally to countries in the LAC region, the data set contains data for countries in other regions like Europe. To perform a successful analysis for the LAC region, these other countries need to be filtered out by using the provided additional Sheet containing country meta data like the region. The data is openly available under the CC BY-4.0 license.  
Because this dataset includes less data than Datasource1, the analysis can only be performed for the years 2000-2021 which should still be a sufficient amount of data to answer the given research question.

## Work Packages

1. Data Preprocessing [#1][i1]
2. Data Cleaning [#2][i2]
3. Data Exploration [#3][i3]
4. Data Analysis [#4][i4]
5. Write Project Report [#5][i5]

[i1]: https://github.com/users/Faoilthiama/projects/1/views/1?pane=issue&itemId=85529288
[i2]: https://github.com/users/Faoilthiama/projects/1/views/1?pane=issue&itemId=85658561
[i3]: https://github.com/users/Faoilthiama/projects/1/views/1?pane=issue&itemId=85658567
[i4]: https://github.com/users/Faoilthiama/projects/1/views/1?pane=issue&itemId=85658575
[i5]: https://github.com/users/Faoilthiama/projects/1/views/1?pane=issue&itemId=85658587
