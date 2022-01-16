import unittest

from party import app
from model import db, example_data, connect_to_db


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"board games, rainbows, and ice cream sundaes", result.data)
        
    def test_no_rsvp_yet(self):
        # FIXME: Add a test to show we see the RSVP form, but NOT the
        # party details
        result = self.client.get("/rsvp")
        self.assertNotIn(b"I have so many fun games!", result.data)
        result2 = self.client.get("/")
        self.assertIn(b"Please RSVP", result2.data)

    def test_rsvp(self):
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)
        # FIXME: Once we RSVP, we should see the party details, but
        # not the RSVP form
        self.assertNotIn(b"Please RSVP", result.data)
        self.assertIn(b"I have so many fun games!", result.data)

class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

        # allows the test to work with the redirect in /games
        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = True

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_games(self):
        result = self.client.get("/games")
        self.assertIn(b"Chess", result.data)
        


if __name__ == "__main__":
    unittest.main()
