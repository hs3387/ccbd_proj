import pandas as pd
from itertools import combinations
from gensim.models import Word2Vec

def list_creation(path):
    # Example table with dress recommendations
    xls = pd.ExcelFile(path)
    df_color = pd.read_excel(xls, 'Sheet4')
    df_dress = pd.read_excel(xls, 'Sheet5')


    color_input = []
    dress_input = []

    color_output = []
    dress_output = []

    for i, row in df_color.iterrows():  
        color_input.append(row['Colour 1'])
        color_output.append(row['Colour 2'])

    for i, row in df_dress.iterrows(): 
        dress_input.append(row['Dress 1'])
        dress_output.append(row['Dress 2'])

    print(color_input)
    print(color_output)
    print(dress_input)
    print(dress_output)

    input_dresses = []
    output_dresses = []
    for color in color_input:
        for dress in dress_input:
            input_dresses.append(color + ' ' + dress)

    for color in color_output:
        for dress in dress_output:
            output_dresses.append(color + ' ' + dress)

    return color_input, color_output, dress_input, dress_output

def color_vetorize(color_input, color_output, test_input):
    # Define a list of sentences
    sentences = color_input + color_output

    # Train a Word2Vec model
    model = Word2Vec([sentences], vector_size=50, window=2, min_count=1, workers=4)

    # Get the embedding for a word
    embedding = model.wv[test_input]

    # Find the most similar words to a given word
    similar_words = model.wv.most_similar(test_input)

    return similar_words

def dress_vectorize(dress_input, dress_output, test_input):
    # Define a list of sentences
    sentences = dress_input + dress_output

    # Train a Word2Vec model
    model = Word2Vec([sentences], vector_size=50, window=2, min_count=1, workers=4)

    # Get the embedding for a word
    embedding = model.wv[test_input]

    # Find the most similar words to a given word
    similar_words = model.wv.most_similar(test_input)

    return similar_words
    
    
file_path = '/content/Fashion Recommendation Table.xlsx'

colorORdress = 'color' # OR 'dress'
test_input = 'Forest Green'

color_input, color_output, dress_input, dress_output = list_creation(file_path)

if colorORdress == 'color':
    color_similarity = color_vetorize(color_input, color_output, test_input )
else:
    dress_similarity = color_vetorize(dress_input, dress_output, test_input )

