import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# df = pd.read_csv(
#     r'C:\Users\nisch\OneDrive\Desktop\New folder\fyp_django-master\store\Books.csv',
#     encoding='utf-8',
#     dtype={'Year-Of-Publication': 'str'},
#     low_memory=False
# )   

# df.columns = df.columns.str.strip()

# print("Columns in DataFrame:", df.columns)

# if 'Book-Title' not in df.columns:
#     print("Column 'Book-Title' not found!")

# common_books_df = pd.read_csv(
#      r'C:\Users\nisch\OneDrive\Desktop\New folder\fyp_django-master\store\Common_Books.csv', 
#     encoding='utf-8'
# )
# rare_books_df = pd.read_csv(
#     r'C:\Users\nisch\OneDrive\Desktop\New folder\fyp_django-master\store\Rare_Books.csv', 
#     encoding='utf-8'
# )  

# def recommend(df, book_title):
#     print("Columns available in the dataframe:", df.columns)  
#     book_title = str(book_title)

#     if 'Book-Title' not in df.columns:
#         print("Column 'Book-Title' not found!")  
#         return []

    
#     if book_title in df['Book-Title'].values:
#         print(f"Found book: {book_title}")  

        
#         rating_count = pd.DataFrame(df["Book-Title"].value_counts())
#         rare_books = rating_count[rating_count["count"] <= 100].index
#         common_books = df[~df["Book-Title"].isin(rare_books)]

#         if book_title in rare_books:
#             print("rare books")
#             most_common = pd.Series(common_books["Book-Title"].unique())
#             if most_common.size >= 3:
#                 most_common = most_common.sample(3).values
#             else:
#                 most_common = most_common.values  
#                 books = list(most_common)
#             return books
#         else:

#             common_books = common_books.drop_duplicates(subset=["Book-Title"])
#             common_books.reset_index(inplace=True)
#             common_books["index"] = [i for i in range(common_books.shape[0])]
            
#             targets = ["Book-Title", "Book-Author", "Publisher"]
#             common_books["all_features"] = [" ".join(common_books[targets].iloc[i,].values) for i in range(common_books[targets].shape[0])]

#             vectorizer = CountVectorizer()
#             common_booksVector = vectorizer.fit_transform(common_books["all_features"])
#             similarity = cosine_similarity(common_booksVector)
            
#             index = common_books[common_books["Book-Title"] == book_title]["index"].values[0]
#             similar_books = list(enumerate(similarity[index]))
#             similar_booksSorted = sorted(similar_books, key=lambda x: x[1], reverse=True)[1:5]
            
#             books = []
#             for i in range(len(similar_booksSorted)):
#                 book = common_books[common_books["index"] == similar_booksSorted[i][0]]["Book-Title"].item()
#                 books.append(book)
                
#             print("Similar books:", books)  
#             return books
#     else:
#         print(f"Book '{book_title}' not found in the dataset!")  
#         return []

df = pd.read_csv(r'store/Books.csv', encoding='utf-8', dtype={'Year-Of-Publication': 'str'}, low_memory=False)

combined_df = pd.concat([df], ignore_index=True)
combined_df.columns = combined_df.columns.str.strip()

def recommend(db_books_df, book_title):
    if book_title not in db_books_df['name'].values:
        return []

    db_books_df['combined'] = db_books_df[['name', 'author', 'publication']].apply(lambda x: ' '.join(str(i) for i in x), axis=1)

    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(db_books_df['combined'])

    db_index = db_books_df[db_books_df['name'] == book_title].index[0]
    db_vector = vectorizer.transform([db_books_df.loc[db_index, 'combined']])
    similarity_scores = cosine_similarity(db_vector, vectors).flatten()
    print(similarity_scores)
    top_matches = similarity_scores.argsort()[-6:-1][::-1]
    recommended_books = db_books_df.iloc[top_matches]['name'].tolist()

    return recommended_books