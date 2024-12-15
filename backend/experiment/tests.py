from django.db import models
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from appuser.models import User, UserProfile
from experiment.models import Experiment

from decimal import Decimal


# Create your tests here.
class ExperimentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # ----create users
        # user1
        publisher = User(
            uid=1000001,
            username="publisher",
            email="123456@qq.com",
            is_active=True,
            is_staff=False,
        )

        publisher.set_password("123456")

        publisher.save()
        userprofile = UserProfile(user=publisher, nickname="user1000001", point=0)
        userprofile.save()

        # user2
        volunteer = User(
            uid=1000002,
            username="volunteer",
            email="1234567@qq.com",
            is_active=True,
            is_staff=False,
        )

        volunteer.set_password("1234567")

        volunteer.save()
        userprofile = UserProfile(user=volunteer, nickname="user1000002", point=0)
        userprofile.save()

        # ----create exps
        # new one
        exp = Experiment(
            title="test",
            description="a discription",
            status="open",
            creator=publisher,
            person_wanted=10,
            person_already=2,
            money_per_person=Decimal(2.5),
            money_paid=Decimal(25),
            money_left=Decimal(20),
        )
        exp.save()

        exp = Experiment(
            title="tesy",
            description="a discription",
            status="open",
            creator=publisher,
            person_wanted=10,
            person_already=2,
            money_per_person=Decimal(2.5),
            money_paid=Decimal(25),
            money_left=Decimal(20),
        )
        exp.save()

    def test_experiments_list_success(self):
        response = self.client.get(reverse("experiment-list"))
        print("\n\033[37;42mtest successful experiment list...\033[0m")
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_experiments_detail_success(self):
        max_id = Experiment.objects.all().aggregate(models.Max("id"))["id__max"]
        response = self.client.get(reverse("experiment-detail", kwargs={"pk": max_id}))
        print("\n\033[37;42mtest successful experiment detail...\033[0m")
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_experiments_detail_failed(self):
        max_id = Experiment.objects.all().aggregate(models.Max("id"))["id__max"]
        response = self.client.get(
            reverse("experiment-detail", kwargs={"pk": max_id + 1})
        )
        print("\n\033[37;42mtest experiment detail -dont exist...\033[0m")
        print(response.content)
        self.assertEqual(response.status_code, 404)

    def test_experiments_create_success(self):
        publisher = User.objects.get(username="publisher")
        self.client.force_authenticate(user=publisher)

        response = self.client.post(
            reverse("experiment-create"),
            data={
                "title": "success",
                "description": "anothe description",
                "person_wanted": 2,
                "money_per_person": 10,
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_experiments_create_failed_date_format(self):
        publisher = User.objects.get(username="publisher")
        self.client.force_authenticate(user=publisher)

        response = self.client.post(
            reverse("experiment-create"),
            data={
                "title": "success",
                "description": "anothe description",
                "person_wanted": 2,
                "money_per_person": 10,
                "activity_time": "19581355",
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_experiments_create_failed_not_login(self):
        response = self.client.post(
            reverse("experiment-create"),
            data={
                "title": "success",
                "description": "anothe description",
                "person_wanted": 2,
                "money_per_person": 10,
            },
        )

        self.assertEqual(response.status_code, 401)

    def test_experiments_search_success(self):
        print("\n\033[37;42mtest successful experiment search...\033[0m")
        response = self.client.get(
            reverse("experiment-search"),
            data={
                "title": "es",
                "description": "a",
                "orderby": "title",
                "sort": "desc",
            },
        ).json()

        print("\n\033[32mresponse:\033[0m")
        print(response)
        self.assertEqual(response.get("count"), 2)

        print("\n\033[32mresults:\033[0m")
        results = response.get("results")
        print(results)

        print("\n\033[32mfirst item:\033[0m")
        item = results[0]
        print(item)

        self.assertEqual(item["title"], "tesy")
        #
