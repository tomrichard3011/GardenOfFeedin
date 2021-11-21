from django.test import TestCase
from gardenApp.models import *
from utils.Geo import *
from utils.Search import *
from datetime import date
from django.contrib.auth.hashers import PBKDF2PasswordHasher, check_password

# Create your tests here.

# TODO Test links
# internal link
# external links

# TODO Forms
# field validation
# error message
# optional and mandatory fields

class databaseTest(TestCase):
    # database creation/retrieval
    def setUp(self):
        john = PublicUser.objects.create(
            email="john@doe.com",
            username="username",
            pass_hash="hash",
            address="1 Washington Sq, San Jose, CA 95192",
            verified=False,
            latitude=37.4527,
            longitude=-121.9101
        )
        banana = Produce.objects.create(
            produce_name="bananas",
            weight=10.00,
            fruits=True,
            veggies=False,
            owner=john
        )
        Donation.objects.create(
            produce_id=banana,
            reciever=john
        )
        ProduceAlert.objects.create(
            produce_id=banana,
        )

    def test_publicUser(self):
        john = PublicUser.objects.get(email="john@doe.com")
        self.assertEqual(john.email, "john@doe.com")
        self.assertEqual(john.username, "username")
        self.assertEqual(john.pass_hash, "hash")
        self.assertEqual(john.address, "1 Washington Sq, San Jose, CA 95192")
        self.assertFalse(john.verified)
        self.assertEqual(john.latitude, 37.4527)
        self.assertEqual(john.longitude, -121.9101)

    def test_produce(self):
        banana = Produce.objects.get(produce_name="bananas")
        self.assertEqual(banana.produce_name, "bananas")
        self.assertEqual(banana.weight, 10.0)
        self.assertTrue(banana.fruits)
        self.assertFalse(banana.veggies)
        self.assertEqual(banana.owner, PublicUser.objects.get(email="john@doe.com"))

    def test_donation(self):
        donation = Donation.objects.get(reciever=PublicUser.objects.get(username="username"))
        self.assertEqual(donation.produce_id, Produce.objects.get(produce_name="bananas"))
        self.assertEqual(donation.reciever, PublicUser.objects.get(username="username"))


    def test_produceAlert(self):
        alert = ProduceAlert.objects.get(produce_id=Produce.objects.get(produce_name="bananas"))
        self.assertEqual(alert.date_created, date.today())

    #TODO none found tests
    def test_badAccess(self):
        return

    #TODO bad inputs


class geoCodingTest(TestCase):

    def test_addressToCoord(self):
        addr1 = "1 Washington Sq, San Jose, CA 95192"
        location = addressToCoordinates(addr1)
        latitude = 37.3447
        longitude = -121.8910

        self.assertAlmostEqual(location.latitude, latitude, 4)
        self.assertAlmostEqual(location.longitude, longitude, 4)


    def test_badAdress(self):
        addr = "123 bad address City, State"
        with self.assertRaises(Exception) as context:
            addressToCoordinates(addr)
        self.assertTrue("Invalid or Nonexistent address given" in str(context.exception))


    def test_coordDistance(self):
        addr1 = "1 Washington Sq, San Jose, CA 95192"
        addr2 = "200 E Santa Clara St, San Jose, CA 95113"
        actual_distance = .56
        location1 = addressToCoordinates(addr1)
        location2 = addressToCoordinates(addr2)

        calc_distance = coordinateDistance(
            (location1.latitude, location1.longitude),
            (location2.latitude, location2.longitude)
        )
        self.assertEqual(round(calc_distance, 2), actual_distance)



class passwordTest(TestCase):
    def test_hashingFunction(self):
        plaintext = "password"
        salt = "salt"
        hash = "pbkdf2_sha256$260000$salt$BOAEc9gQ0CEXQRxBUdHBbIFI/Fh0OEwXzUsCN5cI+kQ="
        passwordHash = PBKDF2PasswordHasher.encode(
            self=PBKDF2PasswordHasher,
            password=plaintext,
            salt=salt
        )
        self.assertEqual(passwordHash, hash)

    def test_checkHash(self):
        hash = "pbkdf2_sha256$260000$salt$BOAEc9gQ0CEXQRxBUdHBbIFI/Fh0OEwXzUsCN5cI+kQ="
        plaintext = "password"
        self.assertTrue(check_password(plaintext, hash))

    def test_badHash(self):
        hash = "pbkdf2_sha256$260000$salt$BOAEc9gQ0CEXQRxBUdHBbIFI/Fh0OEwXzUsCN5cI+kQ="
        plaintext = "notPassword"
        self.assertFalse(check_password(plaintext, hash))

    def test_incorrectHashFormat(self):
        hash = "notRealHashString"
        plaintext = "password"
        self.assertFalse(check_password(plaintext, hash))


class searchFunction(TestCase):
    def setUp(self):
        PublicUser.objects.create(
            email="john@doe.com",
            username="username1",
            pass_hash="hash",
            address="1 Washington Sq, San Jose, CA 95192",
            verified=False,
            latitude=37.4527,
            longitude=-121.9101
        )

        jane = PublicUser.objects.create(
            email="jane@doe.com",
            username="username2",
            pass_hash="hash",
            address="1 Washington Sq, San Jose, CA 95192",
            verified=False,
            latitude=37.4527,
            longitude=-121.9101
        )

        alice = PublicUser.objects.create(
            email="alice@fake.com",
            username="username3",
            pass_hash="hash",
            address="1 Washington Sq, San Jose, CA 95192",
            verified=False,
            latitude=37.4527,
            longitude=-121.9101
        )

        Produce.objects.create(
            produce_name="bananas",
            weight=10.00,
            fruits=True,
            veggies=False,
            owner=jane
        )

        Produce.objects.create(
            produce_name="bananas",
            weight=10.00,
            fruits=True,
            veggies=False,
            owner=alice
        )

    def test_searchGetLocalUsers(self):
        john = PublicUser.objects.get(email="john@doe.com")
        jane = PublicUser.objects.get(email="jane@doe.com")
        alice = PublicUser.objects.get(email="alice@fake.com")

        self.assertEqual([jane,alice], getLocalUsers(john, 1))

    def test_searchGetLocalProduce(self):
        john = PublicUser.objects.get(email="john@doe.com")
        produce_list = list(Produce.objects.filter(produce_name="bananas"))

        self.assertEqual(produce_list, getLocalProduce(john, "banana", True, False, 1))

    #TODO no search results case

    def test_noResultSearch(self):
        john = PublicUser.objects.get(email="john@doe.com")
        self.assertEqual([], getLocalProduce(john, "does not exist", False, True, 1))

