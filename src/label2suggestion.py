import pandas as pd
from itertools import combinations

def get_dresses():
    # Example table with dress recommendations
    xls = pd.ExcelFile('Fashion Recommendation Table.xlsx')
    df_color = pd.read_excel(xls, 'Sheet4')
    df_dress = pd.read_excel(xls, 'Sheet5')
    
    dresses = list(df_dress['Dress 2'])
    
    return dresses

def get_match(labels):
    # Example table with dress recommendations
    xls = pd.ExcelFile('Fashion Recommendation Table.xlsx')
    df_color = pd.read_excel(xls, 'Sheet4')
    df_dress = pd.read_excel(xls, 'Sheet5')
    
    # Example list of labels  - TO BE INPUT FROM STEP 3
    # labels = ['teal', 'dress'] 

    colors = []
    dresses = []
    for item in labels:
        for i, row in df_color.iterrows():
            if item.lower() in row['Colour 1'].lower().replace(" ",""):
                colors.append(row['Colour 2'])
            
        for i, row in df_dress.iterrows():
            if item.lower() in row['Dress 1'].lower():
                dresses.append(row['Dress 2'])

    # print(colors)
    # print(dresses)

    output = []
    for color in colors:
        for dress in dresses:
            output.append(color + ' ' + dress)

    # print(output)
    return output

# print(get_match(['green','blouse']))

# import pandas as pd
# from itertools import combinations

# # Example table with dress recommendations
# xls = pd.ExcelFile('Fashion Recommendation Table.xlsx')
# df1 = pd.read_excel(xls, 'Sheet1')
# df2 = pd.read_excel(xls, 'Sheet2')

# # Example list of labels  - TO BE INPUT FROM STEP 3
# # labels = ['brown', 'sweater', 'jean'] 
# def get_match(labels):
#     all_combination = [" ".join(a) for a in combinations(labels, 2)]
        
#     # Filter the recommendations based on the labels
#     filtered_df1 = df1[df1['Input Dress'].str.contains('|'.join(all_combination), case=False)]
#     filtered_df2 = df2[df2['Input Dress'].str.contains('|'.join(all_combination), case=False)]

#     # Output matching dress recommendations for each input dress

#     matches = set({})

#     for i in range(len(filtered_df1)):
#         input_dress = filtered_df1.iloc[i]['Input Dress']
#         matching_dress_1 = filtered_df1.iloc[i]['Suggestion']
#         matches.add(matching_dress_1)
#         print(f"For the {', '.join(labels)}, the matching dresses for {input_dress} are: {matching_dress_1}")

#     for i in range(len(filtered_df2)):
#         input_dress = filtered_df2.iloc[i]['Input Dress']
#         matching_dress_1 = filtered_df2.iloc[i]['Matching Dress 1']
#         matching_dress_2 = filtered_df2.iloc[i]['Matching Dress 2']
#         matches.add(matching_dress_1)
#         matches.add(matching_dress_2)
#         print(f"For the {', '.join(labels)}, the matching dresses for {input_dress} are: {matching_dress_1} and {matching_dress_2}.")
    
#     return matches