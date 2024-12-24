from django.db import models
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from appuser.models import User, UserProfile
from experiment.models import Experiment
from relation.models import Engagement

from decimal import Decimal

import inspect


# Create your tests here.
class EngagementTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        # ----create users
        # user1
        self.publisher = User(
            uid=1000001,
            username="publisher",
            email="123456@qq.com",
            is_active=True,
            is_staff=False,
        )

        self.publisher.set_password("123456")

        self.publisher.save()
        userprofile = UserProfile(user=self.publisher, nickname="user1000001", point=0)
        userprofile.save()

        # user2
        self.volunteer1 = User(
            uid=1000002,
            username="volunteer",
            email="1234567@qq.com",
            is_active=True,
            is_staff=False,
        )

        self.volunteer1.set_password("1234567")

        self.volunteer1.save()
        userprofile = UserProfile(user=self.volunteer1, nickname="user1000002", point=0)
        userprofile.save()

        self.volunteer2 = User(
            uid=1000003,
            username="volunteer2",
            email="v1234567@qq.com",
            is_active=True,
            is_staff=False,
        )

        self.volunteer2.set_password("1234567")

        self.volunteer2.save()
        userprofile = UserProfile(user=self.volunteer2, nickname="user1000003", point=0)
        userprofile.save()

        # ----create exps
        # new one
        self.exp1_open_engaged = Experiment(
            title="test",
            description="a discription",
            status="open",
            creator=self.publisher,
            person_wanted=10,
            person_already=2,
            money_per_person=Decimal(2.5),
            money_paid=Decimal(25),
            money_left=Decimal(20),
        )
        self.exp1_open_engaged.save()

        self.exp2_close = Experiment(
            title="tesy",
            description="a discription",
            status="close",
            creator=self.publisher,
            person_wanted=10,
            person_already=2,
            money_per_person=Decimal(2.5),
            money_paid=Decimal(25),
            money_left=Decimal(20),
        )
        self.exp2_close.save()

        self.exp3_open_no_engage = Experiment(
            title="tesy3",
            description="a discription",
            status="open",
            creator=self.publisher,
            person_wanted=10,
            person_already=2,
            money_per_person=Decimal(2.5),
            money_paid=Decimal(25),
            money_left=Decimal(20),
        )
        self.exp3_open_no_engage.save()

        # engage

        self.engage1 = Engagement(
            experiment=self.exp1_open_engaged,
            user=self.volunteer1,
            status="to-qualify-user",
        )

        self.engage2 = Engagement(
            experiment=self.exp1_open_engaged,
            user=self.volunteer2,
            status="to-check-result",
        )

        self.engage1.save()
        self.engage2.save()

    def test_engage_success(self):

        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))

        self.client.force_authenticate(user=self.volunteer1)

        response = self.client.post(
            reverse("experiment-engage"), {"experiment": self.exp3_open_no_engage.id}
        )

        self.assertEqual(response.status_code, 200)

    def test_engage_failed_not_login(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))

        response = self.client.post(
            reverse("experiment-engage"), {"experiment": self.exp3_open_no_engage.id}
        )

        self.assertEqual(response.status_code, 401)

    def test_engage_failed_dont_exist(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        self.client.force_authenticate(user=self.volunteer1)

        response = self.client.post(reverse("experiment-engage"), {"experiment": 0})

        self.assertEqual(response.status_code, 404)

    def test_engage_failed_closed(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        self.client.force_authenticate(user=self.volunteer1)

        response = self.client.post(
            reverse("experiment-engage"), {"experiment": self.exp2_close.id}
        )

        self.assertEqual(response.status_code, 400)

    def test_engage_failed_engaged(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        self.client.force_authenticate(user=self.volunteer1)

        response = self.client.post(
            reverse("experiment-engage"), {"experiment": self.exp1_open_engaged.id}
        )

        self.assertEqual(response.status_code, 400)

    def test_engage_cancel_success(self):  # TODO:
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        self.client.force_authenticate(user=self.volunteer1)
        response = self.client.post(
            reverse("experiment-engage-cancel"),
            {"experiment": self.exp1_open_engaged.id},
        )

        self.assertEqual(response.status_code, 200)
        self.exp1_open_engaged.refresh_from_db()
        self.assertEqual(self.exp1_open_engaged.person_already, 1)

    def test_engage_cancel_failed_not_login(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        response = self.client.post(
            reverse("experiment-engage-cancel"),
            {"experiment": self.exp1_open_engaged.id},
        )

        self.assertEqual(response.status_code, 401)

    def test_engage_cancel_failed_exp_not_exist(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        self.client.force_authenticate(user=self.volunteer1)
        max_id = Experiment.objects.all().aggregate(models.Max("id"))["id__max"]
        response = self.client.post(
            reverse("experiment-engage-cancel"),
            {"experiment": max_id + 1},
        )

        self.assertEqual(response.status_code, 404)

    def test_engage_experiment_search_success(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        self.client.force_authenticate(user=self.volunteer1)
        response = self.client.get(reverse("experiment-engage-search"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), 1)

    def test_engage_experiment_search_failed_not_login(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        response = self.client.get(reverse("experiment-engage-search"))

        self.assertEqual(response.status_code, 401)

    def test_qualify_volunteer_success(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        self.client.force_authenticate(user=self.publisher)
        response = self.client.post(
            reverse("qualify-volunteer"),
            {
                "experiment": self.exp1_open_engaged.id,
                "volunteer": self.volunteer1.username,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), "to-check-result")

    def test_volunteer_list_success(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        self.client.force_authenticate(user=self.publisher)
        response = self.client.get(
            reverse("volunteer-list"), {"experiment": self.exp1_open_engaged.id}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), 2)
