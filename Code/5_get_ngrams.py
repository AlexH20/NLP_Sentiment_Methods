import csv
import sys
from scipy.sparse import csc_matrix,csr_matrix
from sklearn.ensemble import RandomForestRegressor

#To max out field limit
csv.field_size_limit(sys.maxsize)

csv_processed_path = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/processed data/data_processed_wcontrol.csv"
n_gram_path = "/Users/alexanderholzer/PycharmProjects/Thesis/Data/processed data/"

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

def get_ngrams(input_path, output_path):

    with open(input_path, "r") as csv_processed:

        nasdaq_news = csv.reader(csv_processed)

        #Skip header
        next(nasdaq_news, None)

        onegrams = []
        twograms = []

        for item in nasdaq_news:

            print(item[1])

            sentences = item[2].split('.')

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

        filengram = open(output_path + 'NGRAMS_' + '.txt', 'w')

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

def get_sparsematrix_and_car(input_path, ngram_path):

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

    #Open the test or training dataset and build a nested dictionary with count of ngram occurences in dataset
    with open(input_path, "r") as csv_processed:

        nasdaq_news = csv.reader(csv_processed)

        # Skip header
        next(nasdaq_news, None)

        #Get length of dataset
        txt_col_len = len(list(nasdaq_news))

        #Initialize dictionary with as many keys as txt items in dataset
        wrd_dictionary = dict.fromkeys(range(txt_col_len))

        #Initialize dependent variable list (CAR)
        car = []

        csv_processed.close()

        with open(input_path, "r") as csv_processed:

            nasdaq_news = csv.reader(csv_processed)

            #Skip header
            next(nasdaq_news, None)

            for i, item in enumerate(nasdaq_news):

                sentences = item[2].split('.')
                car.append(item[8])

                #Initialize dictionary within dictionary with keys according to all ngrams found in training dataset
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

                        #Add count of found ngrams occurence to dictionary
                        if word0.strip() != '.' and word0.strip() != '':
                            if word0 in wrd_dictionary[i].keys():
                                wrd_dictionary[i][word0] = wrd_dictionary[i][word0] + 1

                            if word1.strip() != '.' and word1.strip() != '':
                                if word0 + ' ' + word1 in wrd_dictionary[i].keys():
                                    wrd_dictionary[i][word0 + ' ' + word1] = wrd_dictionary[i][word0 + ' ' + word1] + 1

        spar_mat = sparse_mat(wrd_dictionary)

    return spar_mat, car

X, y = get_sparsematrix_and_car(csv_processed_path, n_gram_path)

rf=RandomForestRegressor(n_estimators=5000,max_features='sqrt')

rf=rf.fit(X,y)



















