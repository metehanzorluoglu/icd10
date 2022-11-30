import pandas as pd
from tqdm import tqdm

mainFile = 'files/ICD10s.csv'
newColFile = 'files/icd10gm2022syst_kodes.csv'
pd.options.display.max_rows = 1000000


def main():
    newCol = pd.read_csv(newColFile, delimiter=';', low_memory=False)
    mainCsv = pd.read_csv(mainFile, delimiter=';', low_memory=False)

    mainGroup = mainCsv[["ICDCode", "ICDName", "ICDNameTranslated"]]
    group = newCol[["ICDCode", "ICDNameDe"]]

    ''' if you want col index use these
    mainGroup = main.iloc[:, [1, 2, 3]]
    group = newCol.iloc[:, [6, 8]] '''

    mergedGroups = pd.merge(mainGroup, group,
                            on='ICDCode',
                            how='outer')
    fillNan = mergedGroups.fillna('-')
    sort = fillNan.sort_values(by=["ICDCode"], ascending=True)
    reset = sort.reset_index(drop=True)

    data = {'ICDId': [],
            'ICDCode': [],
            'ICDName': [],
            'ICDNameTranslated': [],
            'ICDNameDe': []}

    for index, row in tqdm(reset.iterrows(), total=sort.shape[0], desc="Creating..."):
        data['ICDId'].append(index + 1)
        data['ICDCode'].append(row.ICDCode)
        data['ICDName'].append(row.ICDName)
        data['ICDNameTranslated'].append(row.ICDNameTranslated)
        data['ICDNameDe'].append(row.ICDNameDe)
    newFile = pd.DataFrame(data)
    newFile.to_csv('ICD10s.csv', sep=';', index=False)


if __name__ == '__main__':
    main()
