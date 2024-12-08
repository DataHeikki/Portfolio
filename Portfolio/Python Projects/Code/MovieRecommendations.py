import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to load the dataset
def load_data():
    df = pd.read_csv(r'C:/Users/Heikki/Documents/Portfolio/Data/netflix_titles.csv')
    return df

# Function to handle missing values and preprocess the data
def preprocess_data(df):
    df['description'] = df['description'].fillna('')
    df['listed_in'] = df['listed_in'].fillna('')
    df['content'] = df['description'] + ' ' + df['listed_in']  # Combine text for content-based filtering
    return df

# Function to create the cosine similarity matrix
def build_similarity_matrix(df):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['content'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

# Function to create a dictionary for title-to-index mapping
def create_indices(df):
    indices = pd.Series(df.index, index=df['title']).to_dict()
    return indices

# Function to generate recommendations
def recommend_titles(title, df, indices, cosine_sim, num_recommendations=5, genre_filter='', type_filter=''):
    if title not in indices:
        print("Title not found.")
        return []

    idx = indices[title]  # Get index of the input title
    sim_scores = sorted(list(enumerate(cosine_sim[idx])), key=lambda x: x[1], reverse=True)[1:num_recommendations + 1]

    # Filter recommendations based on genre and type
    recommendations = [
        df.iloc[i[0]]['title']
        for i in sim_scores
        if (genre_filter.lower() in df.iloc[i[0]]['listed_in'].lower() or not genre_filter) and 
           (type_filter.lower() in df.iloc[i[0]]['type'].lower() or not type_filter)
    ]

    return recommendations

# Main function to interact with the user
def main():
    df = load_data()  # Load dataset
    df = preprocess_data(df)  # Preprocess dataset
    cosine_sim = build_similarity_matrix(df)  # Build similarity matrix
    indices = create_indices(df)  # Create title-to-index mapping

    print("Welcome to the Netflix Content Recommendation System!\n")
    print("Type 'exit' anytime to quit.\n")

    while True:
        # Step 1: Ask for movie or TV show title first
        title = input("Enter a movie or TV show title: ").strip()
        if title.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break

        # Step 2: Get user input for genre filter (optional)
        genre_filter = input("Enter genre filter (leave empty for no filter): ").strip()

        # Step 3: Get user input for type filter (optional)
        type_filter = input("Enter type filter (Movie/TV Show, leave empty for no filter): ").strip()

        print(f"\nApplying filters: Genre: {genre_filter.title()} | Type: {type_filter.title()}\n")

        # Step 4: Generate recommendations
        recommendations = recommend_titles(title, df, indices, cosine_sim, genre_filter=genre_filter, type_filter=type_filter)

        if recommendations:
            print(f"\nTop {len(recommendations)} recommendations for '{title}':")
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec}")
        else:
            print("No recommendations found. Try another title or adjust the filters.\n")

# Run the main function to start the program
if __name__ == "__main__":
    main()






