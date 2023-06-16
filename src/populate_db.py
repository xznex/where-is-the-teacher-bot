import datetime
import json

from sqlalchemy.orm import Session

from database import engine
from models.audience import Audience

session = Session(bind=engine)


def populate_db():
    with open("../parser/data_file.json", "r") as f:
        parsed = json.load(f)
        for institute in parsed:
            for day_of_week in parsed[institute]:
                for time in parsed[institute][day_of_week]:

                    start, end = time.replace(" ", "").replace(":", ".").split("-")
                    start_of_class = datetime.time(hour=int(start.split(".")[0]), minute=int(start.split(".")[1]))
                    end_of_class = datetime.time(hour=int(end.split(".")[0]), minute=int(end.split(".")[1]))

                    for parity in parsed[institute][day_of_week][time]:
                        for subject in parsed[institute][day_of_week][time][parity]:
                            audience = parsed[institute][day_of_week][time][parity][subject]

                            new_audience = Audience(
                                audience=audience,
                                event=subject,
                                day_of_week=day_of_week,
                                parity=parity,
                                start_of_class=start_of_class,
                                end_of_class=end_of_class
                            )

                            session.add(new_audience)
        session.commit()


if __name__ == "__main__":
    populate_db()
