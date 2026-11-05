from datetime import date

import pytest

from database import MovieModel


@pytest.mark.asyncio
async def test_pagination_links_follow_real_routes(client, db_session):
    for number in range(1, 4):
        db_session.add(MovieModel(
            name=f"Movie {number}", date=date(2020, 1, number), score=7.5,
            genre="Drama", overview="Overview", crew="Crew",
            orig_title=f"Movie {number}", status="Released", orig_lang="en",
            budget=12.50, revenue=30.5, country="US",
        ))
    await db_session.commit()

    first = await client.get("/api/v1/theater/movies/?per_page=1")
    assert first.status_code == 200
    first_data = first.json()
    assert (first_data["total_items"], first_data["total_pages"]) == (3, 3)
    assert first_data["prev_page"] is None
    assert isinstance(first_data["movies"][0]["budget"], (int, float))
    assert isinstance(first_data["movies"][0]["revenue"], (int, float))

    second = await client.get(first_data["next_page"])
    assert second.status_code == 200
    second_data = second.json()
    assert [first_data["movies"][0]["id"], second_data["movies"][0]["id"]] == [1, 2]
    assert (await client.get(second_data["prev_page"])).json() == first_data

    third = await client.get(second_data["next_page"])
    assert third.status_code == 200
    assert third.json()["movies"][0]["id"] == 3
    assert third.json()["next_page"] is None
    assert (await client.get("/api/v1/theater/movies/?page=4&per_page=1")).status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize("query, field", [
    ("page=0", "page"), ("page=abc", "page"),
    ("per_page=0", "per_page"), ("per_page=21", "per_page"),
])
async def test_invalid_pagination_parameters_identify_the_field(client, query, field):
    response = await client.get(f"/api/v1/theater/movies/?{query}")
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", field]
