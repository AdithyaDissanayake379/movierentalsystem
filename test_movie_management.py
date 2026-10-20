
# ============================================================
# MOVIE RENTAL MANAGEMENT SYSTEM
# Movie Management Testing Script
# ============================================================

from modules.movie_management import (
    add_movie,
    view_movies,
    update_movie,
    delete_movie,
    search_movies
)


def display_movies(movie_records):
    """
    Print movie records in a readable format.
    """

    if not movie_records:
        print("No movies found.")
        return

    for movie in movie_records:
        print("-" * 55)
        print("Movie ID:", movie["movie_id"])
        print("Title:", movie["title"])
        print("Genre:", movie["genre"])
        print("Release Year:", movie["release_year"])
        print("Rental Price:", movie["rental_price"])
        print("Producer:", movie["producer"])
        print("Status:", movie["status"])


def main():

    # Unique ID returned by the database
    test_movie_id = None

    try:
        print("\n========== TEST 1: ADD MOVIE ==========")

        test_movie_id = add_movie(
            "Inception",
            "Science Fiction",
            2010,
            350.00,
            "Emma Thomas"
        )

        print("Movie inserted successfully.")
        print("New Movie ID:", test_movie_id)

        print("\n========== TEST 2: VIEW MOVIES ==========")

        all_movies = view_movies()
        display_movies(all_movies)

        print("\n========== TEST 3: SEARCH MOVIE ==========")

        results = search_movies(
            title="Inception"
        )
        display_movies(results)

        print("\n========== TEST 4: UPDATE MOVIE ==========")

        update_movie(
            test_movie_id,
            "Inception",
            "Sci-Fi",
            2010,
            400.00,
            "Emma Thomas"
        )

        print("Movie updated successfully.")

        print("\n========== TEST 5: VERIFY UPDATE ==========")

        results = search_movies(
            title="Inception"
        )

        display_movies(results)

        print("\n========== TEST 6: FILTER MOVIES ==========")

        results = search_movies(
            genre="Sci-Fi",
            year=2010,
            min_price=300,
            max_price=500
        )

        display_movies(results)

        print("\n========== TEST 7: DELETE MOVIE ==========")

        delete_movie(test_movie_id)

        print("Movie deleted successfully.")

        print("\n========== TEST 8: VERIFY DELETION ==========")

        remaining = [
            movie for movie in view_movies()
            if movie["movie_id"] == test_movie_id
        ]

        if not remaining:
            print("PASS: Movie is no longer in the database.")
        else:
            print("FAIL: Movie still exists.")

    except Exception as error:
        print("\nTEST ERROR:", error)
        print("Review the output above for the failing step.")


if __name__ == "__main__":
    main()
