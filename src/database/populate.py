import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from tqdm import tqdm

from src.config import get_settings
from src.database import MovieModel, get_db_contextmanager


class CSVDatabaseSeeder:
    def __init__(self, csv_file_path: str, db_session: Session):
        self._csv_file_path = csv_file_path
        self._db_session = db_session

    def is_db_populated(self) -> bool:
        return self._db_session.query(MovieModel).first() is not None

    def _preprocess_csv(self):
        data = pd.read_csv(self._csv_file_path)
        data = data.drop_duplicates(subset=['names', 'date_x'], keep='first')
        data['crew'] = data['crew'].fillna('Unknown')
        data['genre'] = data['genre'].fillna('Unknown')
        data['genre'] = data['genre'].str.replace('\u00A0', '', regex=True)
        data['date_x'] = data['date_x'].str.strip()
        data['date_x'] = pd.to_datetime(data['date_x'], format='%m/%d/%Y', errors='raise')
        data['date_x'] = data['date_x'].dt.date
        print("Preprocessing csv file")

    def seed(self):
        try:
            if self._db_session.in_transaction():
                print("Rolling back existing transaction.")
                self._db_session.rollback()

            self._preprocess_csv()

            data = pd.read_csv(self._csv_file_path)
            data['date_x'] = pd.to_datetime(data['date_x']).dt.date

            with self._db_session.begin():
                for _, row in tqdm(data.iterrows(), total=data.shape[0], desc="Seeding database"):

                    movie = MovieModel(
                        name=row['names'],
                        date=row['date_x'],
                        score=float(row['score']),
                        genre=row['genre'],
                        overview=row['overview'],
                        crew=row['crew'],
                        orig_title=row['orig_title'],
                        status=row['status'],
                        orig_lang=row['orig_lang'],
                        budget=float(row['budget_x']),
                        revenue=float(row['revenue']),
                        country=row['country']
                    )
                    self._db_session.add(movie)
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise


def main():
    settings = get_settings()
    with get_db_contextmanager() as db_session:
        seeder = CSVDatabaseSeeder(settings.PATH_TO_MOVIES_CSV, db_session)

        if not seeder.is_db_populated():
            try:
                seeder.seed()
                print("Database seeding completed successfully.")
            except Exception as e:
                print(f"Failed to seed the database: {e}")
        else:
            print("Database is already populated. Skipping seeding.")


if __name__ == "__main__":
    main()
