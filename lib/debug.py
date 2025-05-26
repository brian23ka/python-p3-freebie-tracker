# debug.py

from models import Company, Dev, Freebie, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import ipdb

# Setup database connection and session
engine = create_engine('sqlite:///freebies.db')
Base.metadata.create_all(engine)  # Creates tables if not exist

Session = sessionmaker(bind=engine)
session = Session()

# Sample test code to create and query objects
def seed_data():
    # Clear existing data
    session.query(Freebie).delete()
    session.query(Dev).delete()
    session.query(Company).delete()
    session.commit()

    # Create companies
    c1 = Company(name="Acme Corp", founding_year=1990)
    c2 = Company(name="Globex Inc", founding_year=1985)
    session.add_all([c1, c2])

    # Create devs
    d1 = Dev(name="Alice")
    d2 = Dev(name="Bob")
    session.add_all([d1, d2])
    session.commit()

    # Give freebies
    freebie1 = c1.give_freebie(d1, "T-Shirt", 10)
    freebie2 = c2.give_freebie(d1, "Coffee Mug", 15)
    freebie3 = c1.give_freebie(d2, "Sticker", 5)
    session.add_all([freebie1, freebie2, freebie3])
    session.commit()

    print(freebie1.print_details())
    print(freebie2.print_details())
    print(freebie3.print_details())

def test_relationships():
    alice = session.query(Dev).filter_by(name="Alice").first()
    print(f"{alice.name}'s freebies:")
    for freebie in alice.freebies:
        print(f" - {freebie.item_name} from {freebie.company.name}")

    acme = session.query(Company).filter_by(name="Acme Corp").first()
    print(f"{acme.name}'s freebies:")
    for freebie in acme.freebies:
        print(f" - {freebie.item_name} owned by {freebie.dev.name}")

    oldest = Company.oldest_company(session)
    print(f"The oldest company is {oldest.name}, founded in {oldest.founding_year}")

if __name__ == '__main__':
    seed_data()
    test_relationships()

    # Enter interactive ipdb shell for manual testing
    ipdb.set_trace()

