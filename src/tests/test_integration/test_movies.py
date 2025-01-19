import random

import pytest

from src.database import MovieModel


def test_get_movies_empty_database(client):
    response = client.get("/api/v1/theater/movies/")

    assert response.status_code == 404
    assert response.json() == {"detail": "No movies found."}


def test_get_movies_default_parameters(client, seed_database):
    response = client.get("/api/v1/theater/movies/")

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    response_data = response.json()

    assert len(response_data["movies"]) == 10
    assert response_data["total_pages"] > 0
    assert response_data["total_items"] > 0

    assert response_data["prev_page"] is None

    if response_data["total_pages"] > 1:
        assert response_data["next_page"] is not None


def test_get_movies_with_custom_parameters(client, seed_database):
    page = 2
    per_page = 5

    response = client.get(f"/api/v1/theater/movies/?page={page}&per_page={per_page}")

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    response_data = response.json()

    assert len(response_data["movies"]) == per_page

    assert response_data["total_pages"] > 0
    assert response_data["total_items"] > 0

    if page > 1:
        assert response_data["prev_page"] == f"/theater/movies/?page={page - 1}&per_page={per_page}"
    if page < response_data["total_pages"]:
        assert response_data["next_page"] == f"/theater/movies/?page={page + 1}&per_page={per_page}"
    else:
        assert response_data["next_page"] is None


@pytest.mark.parametrize("page, per_page, expected_detail", [
    (0, 10, "Input should be greater than or equal to 1"),
    (1, 0, "Input should be greater than or equal to 1"),
    (0, 0, "Input should be greater than or equal to 1"),
])
def test_invalid_page_and_per_page(client, page, per_page, expected_detail):
    response = client.get(f"/api/v1/theater/movies/?page={page}&per_page={per_page}")

    assert response.status_code == 422

    response_data = response.json()
    assert "detail" in response_data

    assert any(expected_detail in error["msg"] for error in response_data["detail"])


def test_per_page_maximum_allowed_value(client, seed_database):
    response = client.get("/api/v1/theater/movies/?page=1&per_page=20")

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    response_data = response.json()

    assert "movies" in response_data, "Response missing 'movies' field."
    assert len(response_data["movies"]) <= 20, (
        f"Expected at most 20 movies, but got {len(response_data['movies'])}"
    )


def test_page_exceeds_maximum(client, db_session, seed_database):
    per_page = 10
    total_movies = db_session.query(MovieModel).count()
    max_page = (total_movies + per_page - 1) // per_page

    response = client.get(f"/api/v1/theater/movies/?page={max_page + 1}&per_page={per_page}")

    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"

    response_data = response.json()

    assert "detail" in response_data, "Response missing 'detail' field."
    assert response_data["detail"] == "No movies found.", (
        f"Expected 'No movies found.', but got: {response_data['detail']}"
    )


def test_movie_list_with_pagination(client, db_session, seed_database):
    page = 2
    per_page = 5
    offset = (page - 1) * per_page

    response = client.get(f"/api/v1/theater/movies/?page={page}&per_page={per_page}")

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    response_data = response.json()

    total_items = db_session.query(MovieModel).count()
    total_pages = (total_items + per_page - 1) // per_page
    assert response_data["total_items"] == total_items, "Total items mismatch."
    assert response_data["total_pages"] == total_pages, "Total pages mismatch."

    expected_movies = (
        db_session.query(MovieModel)
        .offset(offset)
        .limit(per_page)
        .all()
    )
    expected_movie_ids = [movie.id for movie in expected_movies]
    returned_movie_ids = [movie["id"] for movie in response_data["movies"]]

    assert expected_movie_ids == returned_movie_ids, "Movies on the page mismatch."

    assert response_data["prev_page"] == (
        f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    ), "Previous page link mismatch."
    assert response_data["next_page"] == (
        f"/theater/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None
    ), "Next page link mismatch."


def test_get_movie_by_id_not_found(client):
    movie_id = 1

    response = client.get(f"/api/v1/theater/movies/{movie_id}")

    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"

    response_data = response.json()
    assert response_data == {"detail": "Movie with the given ID was not found."}, (
        f"Expected error message not found. Got: {response_data}"
    )


def test_get_movie_by_id_valid(client, db_session, seed_database):
    min_id = db_session.query(MovieModel.id).order_by(MovieModel.id.asc()).first()[0]
    max_id = db_session.query(MovieModel.id).order_by(MovieModel.id.desc()).first()[0]

    random_id = random.randint(min_id, max_id)

    expected_movie = db_session.query(MovieModel).filter(MovieModel.id == random_id).first()
    assert expected_movie is not None, "Movie not found in database."

    response = client.get(f"/api/v1/theater/movies/{random_id}")

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    response_data = response.json()
    assert response_data["id"] == expected_movie.id, "Returned ID does not match the requested ID."
    assert response_data["name"] == expected_movie.name, "Returned name does not match the expected name."
    assert response_data["date"] == str(expected_movie.date), "Returned date does not match the expected date."
    assert response_data["score"] == expected_movie.score, "Returned score does not match the expected score."
    assert response_data["genre"] == expected_movie.genre, "Returned genre does not match the expected genre."
    assert response_data["overview"] == expected_movie.overview, ("Returned overview does not match the expected "
                                                                  "overview.")
    assert response_data["crew"] == expected_movie.crew, "Returned crew does not match the expected crew."
    assert response_data["orig_title"] == expected_movie.orig_title, ("Returned original title does not match the "
                                                                      "expected title.")
    assert response_data["status"] == expected_movie.status, "Returned status does not match the expected status."
    assert response_data["orig_lang"] == expected_movie.orig_lang, ("Returned original language does not match the "
                                                                    "expected language.")
    assert response_data["budget"] == float(expected_movie.budget), ("Returned budget does not match the "
                                                                     "expected budget.")
    assert response_data["revenue"] == expected_movie.revenue, "Returned revenue does not match the expected revenue."
    assert response_data["country"] == expected_movie.country, "Returned country does not match the expected country."
