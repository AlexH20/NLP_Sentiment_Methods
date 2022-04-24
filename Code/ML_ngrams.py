import csv
import sys
from scipy.sparse import csc_matrix,csr_matrix
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

#To max out field limit
csv.field_size_limit(sys.maxsize)

input_path = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/processed data/descriptive data/"
input_file = "sorted_processed_data.csv"
n_gram_path = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/processed data/"

data = pd.read_csv(input_path + input_file, index_col = False)

#Create a sparse matrix with the dictionary returned by the function get_ngrams Frankel, Jennings and Lee (2021) (modified for own needs)

def sparse_mat(data):
    row1 = []
    col1 = []
    data1 = []

    for key, value in data.items():

        value_n = list(value.values())

        for e, elem in enumerate(value_n):
            colnum = e
            value = elem

            row1.append(key)
            col1.append(colnum)
            data1.append(value)

    X = csc_matrix((data1, (row1, col1)))  # Sparse matrix of rows (observations) and columns (independent variables)

    return X

#Function to get n_grams count of whole training data set
#This function will iterate over all text items in the training data set and return all possible one- and twograms within the training data

def get_ngrams(data, ngram_path):

    onegrams = []
    twograms = []

    for index, row in data.iterrows():

        sentences = row["Text"].split('.')

        #### EXTRACT ALL ONE AND TWO WORD PHRASES #### Frankel, Jennings and Lee (2021)

        for sentence in sentences:

            sentence = sentence.replace('.', '').strip()

            allwords = sentence.split(' ')

            for w, word in enumerate(allwords):
                word0 = allwords[w]
                try:
                    word1 = allwords[w + 1]
                except Exception:
                    word1 = ''

                if word0.strip() != '.' and word0.strip() != '':
                    onegrams.append(word0)

                    if word1.strip() != '.' and word1.strip() != '':
                        twogram = word0 + ' ' + word1
                        twograms.append(twogram)

    filengram = open(ngram_path + 'NGRAMS_' + '.txt', 'w')

    uniqueonegrams = list(set(onegrams))
    uniqueonegrams = sorted(uniqueonegrams)
    for uniqueonegram in uniqueonegrams:
        count = onegrams.count(uniqueonegram)
        filengram.write(uniqueonegram + '|' + repr(count) + '\n')

    uniquetwograms = list(set(twograms))
    uniquetwograms = sorted(uniquetwograms)
    for uniquetwogram in uniquetwograms:
        count = twograms.count(uniquetwogram)
        filengram.write(uniquetwogram + '|' + repr(count) + '\n')

    filengram.close()



#The function get_ngrams_eachtxt_sparsematrix takes the ngram_file with all one- and twograms from the function above
#and iterates again over each text item (either training or test data) to count occurence of the words from the ngram file.
#This function returns a nested dictionary which represents for each txt item in dataset the training dataset ngram occurences

def get_sparsematrix_and_car(data, ngram_path):

    #Get all one- and twograms from training dataset and turn them into a list
    with open(ngram_path + 'NGRAMS_' + '.txt') as ngram_file:

        wrd_list = []

        for wrd in ngram_file:

            if wrd not in wrd_list:
                wrd = wrd.replace('\n', ' ')
                wrd = wrd.split('|')

                wrd_list.append(wrd[0])

        wrd_list = sorted(wrd_list)
        wrd_list = tuple(wrd_list)

    ngram_file.close()

    # Get length of dataset
    txt_col_len = len(data)

    # Initialize dictionary with as many keys as txt items in dataset
    wrd_dictionary = dict.fromkeys(range(txt_col_len))

    # Initialize dependent variable list (CAR)
    car = []

    for index, row in data.iterrows():

        sentences = data["Text"].split('.')
        #car.append(data["CAR"])

        # Initialize dictionary within dictionary with keys according to all ngrams found in training dataset. Frankel, Jennings and Lee (2021) (modified for own needs)
        wrd_dictionary[i] = dict.fromkeys(wrd_list, 0)

        for sentence in sentences:

            sentence = sentence.replace('.', '').strip()
            allwords = sentence.split(' ')

            for w, word in enumerate(allwords):
                word0 = allwords[w]
                try:
                    word1 = allwords[w + 1]
                except Exception:
                    word1 = ''

                # Add count of found ngrams occurence to dictionary
                if word0.strip() != '.' and word0.strip() != '':
                    if word0 in wrd_dictionary[i].keys():
                        wrd_dictionary[i][word0] = wrd_dictionary[i][word0] + 1

                    if word1.strip() != '.' and word1.strip() != '':
                        if word0 + ' ' + word1 in wrd_dictionary[i].keys():
                            wrd_dictionary[i][word0 + ' ' + word1] = wrd_dictionary[i][word0 + ' ' + word1] + 1

    spar_mat = sparse_mat(wrd_dictionary)

    return spar_mat, car

def split_years(dt):
    dt["Year"] = dt["Date"].dt.year
    return [dt[dt["Year"] == y] for y in dt["Year"].unique()]

def split_weeks(dt):
    dt["Week"] = dt["Date"].dt.isocalendar().week
    return [dt[dt["Week"] == y] for y in dt["Week"].unique()]

data_splt_years = split_years(data)

for year in sorteddflist:
    year = split_weeks(year)
    for i, week in enumerate(year):

        get_ngrams(year[i], n_gram_path)

        X_train, y_train = get_sparsematrix_and_car(year[i], n_gram_path)
        X_test, y_test = get_sparsematrix_and_car(year[i+1], n_gram_path)

        rf = RandomForestRegressor(n_estimators=5000, max_features='sqrt')

        rf = rf.fit(X_train, y_train)
        predictions = rf.predict(X_test)























