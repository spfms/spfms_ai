import pandas as pd


def main():
    df = pd.read_csv('../datasets/stocknews/Combined_News_DJIA.csv', encoding="ISO-8859-1")
    train = df[df['Date'] < '20150101']
    test = df[df['Date'] > '20141231']

    # Removing punctuations
    data = train.iloc[:, 2:27]
    data.replace("[^a-zA-Z]", " ", regex=True, inplace=True)

    # Renaming column names for ease of access
    list1 = [i for i in range(25)]
    new_Index = [str(i) for i in list1]
    data.columns = new_Index

    # Convertng headlines to lower case
    for index in new_Index:
        data[index] = data[index].str.lower()

    headlines = []
    for row in range(0, len(data.index)):
        headlines.append(' '.join(str(x) for x in data.iloc[row, 0:25]))

    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.ensemble import RandomForestClassifier

    ## implement BAG OF WORDS
    countvector = CountVectorizer(ngram_range=(2, 2))
    traindataset = countvector.fit_transform(headlines)

    # implement RandomForest Classifier
    randomclassifier = RandomForestClassifier(n_estimators=200, criterion='entropy')
    randomclassifier.fit(traindataset, train['Label'])

    ## Predict for the Test Dataset
    test_transform = []
    for row in range(0, len(test.index)):
        test_transform.append(' '.join(str(x) for x in test.iloc[row, 2:27]))
    test_dataset = countvector.transform(test_transform)
    predictions = randomclassifier.predict(test_dataset)

    print(randomclassifier.predict(countvector.fit_transform("stock will be terrible tomorrow")))

    ## Import library to check accuracy
    from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

    matrix = confusion_matrix(test['Label'], predictions)
    print(matrix)
    score = accuracy_score(test['Label'], predictions)
    print(score)
    report = classification_report(test['Label'], predictions)
    print(report)

    df.to_csv('output.csv')


if __name__ == '__main__':
    main()
