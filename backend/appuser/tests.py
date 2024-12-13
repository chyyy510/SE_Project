from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from appuser.models import User, UserProfile


# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # user1
        user = User(
            uid=1000001,
            username=123456,
            email="123456@qq.com",
            is_active=True,
            is_staff=False,
        )

        user.set_password("123456")

        user.save()
        userprofile = UserProfile(user=user, nickname="user1000001")
        userprofile.save()

        # user2
        user = User(
            uid=1000002,
            username=1234567,
            email="1234567@qq.com",
            is_active=True,
            is_staff=False,
        )

        user.set_password("1234567")

        user.save()
        userprofile = UserProfile(user=user, nickname="user1000002")
        userprofile.save()

    def test_users_list_success(self):
        response = self.client.get(reverse("user-list"))
        print("\n\033[32mtest user list...\033[0m")
        response.content
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_users_register_success(self):
        # right
        print("\n\033[32mtest successful register...\033[0m")
        response = self.client.post(
            reverse("user-register"),
            data={
                "email": "Alice@gmail.com",
                "username": "Alice",
                "password_encrypted": "aNE7O04+KsAjsxtkM+ybDV83iCUxes0ydQdalEGP1zK4mQ7ZtaZBsBc8Lmd6yyW+I7RXz4Hq3E2L3HY9m3Jw3ZQ7zH0Mypuwi/3/bfbxwC5Q4lo1gF5FS2yK9NsQndl102J5bPWftObh9pKuuxmM3+TRZ44pl/1tsIRwOLrMmlIxmtFk2eCh8RHCetHmZoRQDZ3fg9bfD1XdWdAGYxeF5UC5kYQshaEswltX0fShsRA0ZY+VoJYowotgfmUuyWT9OQ3sRNA3UOwC94lIN1mnNVHcWP2NQ06XMa33eLxrSRTOUsYcL0C+6tYCD4MGu49jrnBsQXDc9GZMtSO7JjROGg==",
            },
        )
        print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 3)

    def test_users_register_failed_email(self):
        # wrong email duplicate
        print("\n\033[32mtest email duplicate...\033[0m")
        response = self.client.post(
            reverse("user-register"),
            data={
                "email": "123456@qq.com",
                "username": "Alice",
                "password_encrypted": "aNE7O04+KsAjsxtkM+ybDV83iCUxes0ydQdalEGP1zK4mQ7ZtaZBsBc8Lmd6yyW+I7RXz4Hq3E2L3HY9m3Jw3ZQ7zH0Mypuwi/3/bfbxwC5Q4lo1gF5FS2yK9NsQndl102J5bPWftObh9pKuuxmM3+TRZ44pl/1tsIRwOLrMmlIxmtFk2eCh8RHCetHmZoRQDZ3fg9bfD1XdWdAGYxeF5UC5kYQshaEswltX0fShsRA0ZY+VoJYowotgfmUuyWT9OQ3sRNA3UOwC94lIN1mnNVHcWP2NQ06XMa33eLxrSRTOUsYcL0C+6tYCD4MGu49jrnBsQXDc9GZMtSO7JjROGg==",
            },
        )
        print(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 2)

    def test_users_register_failed_username(self):
        # wrong username duplicate
        print("\n\033[32mtest username duplicate...\033[0m")
        response = self.client.post(
            reverse("user-register"),
            data={
                "email": "Alice@gmail.com",
                "username": "123456",
                "password_encrypted": "aNE7O04+KsAjsxtkM+ybDV83iCUxes0ydQdalEGP1zK4mQ7ZtaZBsBc8Lmd6yyW+I7RXz4Hq3E2L3HY9m3Jw3ZQ7zH0Mypuwi/3/bfbxwC5Q4lo1gF5FS2yK9NsQndl102J5bPWftObh9pKuuxmM3+TRZ44pl/1tsIRwOLrMmlIxmtFk2eCh8RHCetHmZoRQDZ3fg9bfD1XdWdAGYxeF5UC5kYQshaEswltX0fShsRA0ZY+VoJYowotgfmUuyWT9OQ3sRNA3UOwC94lIN1mnNVHcWP2NQ06XMa33eLxrSRTOUsYcL0C+6tYCD4MGu49jrnBsQXDc9GZMtSO7JjROGg==",
            },
        )

        print(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 2)

    def test_users_login_success(self):
        # right
        print("\n\033[32mtest successful login...\033[0m")
        response = self.client.post(
            reverse("user-login"),
            data={
                "email": "123456@qq.com",
                "password_encrypted": "aNE7O04+KsAjsxtkM+ybDV83iCUxes0ydQdalEGP1zK4mQ7ZtaZBsBc8Lmd6yyW+I7RXz4Hq3E2L3HY9m3Jw3ZQ7zH0Mypuwi/3/bfbxwC5Q4lo1gF5FS2yK9NsQndl102J5bPWftObh9pKuuxmM3+TRZ44pl/1tsIRwOLrMmlIxmtFk2eCh8RHCetHmZoRQDZ3fg9bfD1XdWdAGYxeF5UC5kYQshaEswltX0fShsRA0ZY+VoJYowotgfmUuyWT9OQ3sRNA3UOwC94lIN1mnNVHcWP2NQ06XMa33eLxrSRTOUsYcL0C+6tYCD4MGu49jrnBsQXDc9GZMtSO7JjROGg==",
            },
        )
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_users_login_failed_user_dont_exist(self):
        # wrong user dont exist
        print("\n\033[32mtest email don't exist...\033[0m")
        response = self.client.post(
            reverse("user-login"),
            data={
                "email": "56@qq.com",
                "password_encrypted": "aNE7O04+KsAjsxtkM+ybDV83iCUxes0ydQdalEGP1zK4mQ7ZtaZBsBc8Lmd6yyW+I7RXz4Hq3E2L3HY9m3Jw3ZQ7zH0Mypuwi/3/bfbxwC5Q4lo1gF5FS2yK9NsQndl102J5bPWftObh9pKuuxmM3+TRZ44pl/1tsIRwOLrMmlIxmtFk2eCh8RHCetHmZoRQDZ3fg9bfD1XdWdAGYxeF5UC5kYQshaEswltX0fShsRA0ZY+VoJYowotgfmUuyWT9OQ3sRNA3UOwC94lIN1mnNVHcWP2NQ06XMa33eLxrSRTOUsYcL0C+6tYCD4MGu49jrnBsQXDc9GZMtSO7JjROGg==",
            },
        )
        print(response.content)
        self.assertEqual(response.status_code, 401)

    def test_users_login_failed_wrong_password(self):
        # wrong pwd
        response = self.client.post(
            reverse("user-login"),
            data={
                "email": "123456@qq.com",
                "password_encrypted": "bdOG6lj/+APy6ZlBHjHyQWSqnzWI29UtsAfQPqaJbEWUypEf9lqOFmk1yLKuyds6KmosaKP6PsrKJIa9U1WtVDBhpRMbP+CkS2kNGHF72VQhRfnm1cMnWsSEgrolIGi3FZ+G6hf2Y+NL12kf9RRCRhLqtwWa6hQf7WSNBXQGJ1pktlUNY/Hry3J/kCgSEDZYJHO5bakJFKwQ+hIwuhFbtKsf0th1rTqhojlzJTfwd9nV7OEyQDgSVQ5U5MKSyH2DfsbjVMp5BIEJ1JCq+8uHDyhbawmZdC8JRfj+klwejSWcO8Z95ZISlIvbdkgypPO4Xlboovh0nIGMJmtFkGC5Og==",
            },
        )
        print(response.content)
        self.assertEqual(response.status_code, 401)

    def test_users_profile_detail_success(self):
        # right
        print("\n\033[32mtest successful user profile...\033[0m")

        # --login
        publisher = User.objects.get(username="123456")
        self.client.force_authenticate(user=publisher)

        # --profileTODO:有点问题？
        response = self.client.get(reverse("user-profile"))
        self.assertEqual(response.status_code, 200)

    def test_users_profile_detail_failed_not_login(self):
        # wrong not login
        print("\n\033[32mtest failed user profile...\033[0m")
        response = self.client.get(reverse("user-profile"))
        self.assertEqual(response.status_code, 401)
