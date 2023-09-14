import sqlite3

# Read file content
with open('stephen_king_adaptations.txt', 'r') as file:
    stephen_king_adaptations_list = file.readlines()

# Establish a connection with the SQLite database
connection = sqlite3.connect('stephen_king_adaptations.db')
cursor = connection.cursor()

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
        movieID INTEGER PRIMARY KEY AUTOINCREMENT,
        movieName TEXT,
        movieYear INTEGER,
        imdbRating REAL
    )
''')

# Insert file content into the table
for line in stephen_king_adaptations_list:
    movie_data = line.strip().split(',')
    if len(movie_data) == 4:
        movie_name = movie_data[1].strip()
        movie_year = int(movie_data[2].strip())
        imdb_rating = float(movie_data[3].strip())
        
        cursor.execute('''
            INSERT INTO stephen_king_adaptations_table (movieName, movieYear, imdbRating)
            VALUES (?, ?, ?)
        ''', (movie_name, movie_year, imdb_rating))

# Commit changes and close the connection
connection.commit()
connection.close()

# Interactive queries
while True:
    print("\nPlease select a query parameter:")
    print("1. Movie name")
    print("2. Release year")
    print("3. Rating")
    print("4. Stop")
  
    option = input("Enter your choice: ")

    # Execute the corresponding operation based on user choice
    if option == "1":
        movie_name = input("Enter the movie name to search for: ")
        connection = sqlite3.connect('stephen_king_adaptations.db')
        cursor = connection.cursor()
        cursor.execute('''
            SELECT movieName, movieYear, imdbRating
            FROM stephen_king_adaptations_table
            WHERE movieName = ?
        ''', (movie_name,))
        result = cursor.fetchone()
        if result:
            print("Movie name: ", result[1])
            print("Release year: ", result[2])
            print("Rating: ", result[3])
        else:
            print("The movie is not in our database.")
        connection.close()

    elif option == "2":
        movie_year = int(input("Enter the release year to search for: "))
        connection = sqlite3.connect('stephen_king_adaptations.db')
        cursor = connection.cursor()
        cursor.execute('''
            SELECT movieName, movieYear, imdbRating
            FROM stephen_king_adaptations_table
            WHERE movieYear = ?
        ''', (movie_year,))
        results = cursor.fetchall()
        if results:
            for result in results:
                print("Movie name: ", result[1])
                print("Release year: ", result[2])
                print("Rating: ", result[3])
        else:
            print("No movies were found for that year in our database.")
        connection.close()

    elif option == "3":
        rating = float(input("Enter the minimum rating to search for: "))
        connection = sqlite3.connect('stephen_king_adaptations.db')
        cursor = connection.cursor()
        cursor.execute('''
            SELECT movieName, movieYear, imdbRating
            FROM stephen_king_adaptations_table
            WHERE imdbRating >= ?
        ''', (rating,))
        results = cursor.fetchall()
        if results:
            for result in results:
                print("Movie name: ", result[1])
                print("Release year: ", result[2])
                print("Rating: ", result[3])
        else:
            print("No movies at or above that rating were found in the database.")
        connection.close()

    elif option == "4":
        print("Program terminated.")
        break

    else:
        print("Invalid option, please select again.")
