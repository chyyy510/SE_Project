from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from appuser.models import User, UserProfile

import inspect


# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # user1
        user = User(
            uid=1000001,
            username="publisher",
            email="123456@qq.com",
            is_active=True,
            is_staff=False,
        )

        user.set_password("123456")

        user.save()
        userprofile = UserProfile(user=user, nickname="user1000001", point=0)
        userprofile.save()

        # user2
        user = User(
            uid=1000002,
            username="volunteer",
            email="1234567@qq.com",
            is_active=True,
            is_staff=False,
        )

        user.set_password("1234567")

        user.save()
        userprofile = UserProfile(user=user, nickname="user1000002", point=0)
        userprofile.save()

    def test_users_list_success(self):
        response = self.client.get(reverse("user-list"))
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_users_detail_success(self):
        response = self.client.get(reverse("user-detail"), {"username": "publisher"})
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_users_detail_failed_dont_exist(self):
        response = self.client.get(reverse("user-detail"), {"username": "dont_exist"})
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        print(response.content)
        self.assertEqual(response.status_code, 404)

    def test_users_register_success(self):

        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
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

    def test_users_register_failed_email_duplication(self):

        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
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

    def test_users_register_failed_email_format(self):

        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        response = self.client.post(
            reverse("user-register"),
            data={
                "email": "123456@kcom.",
                "username": "testAlice",
                "password_encrypted": "aNE7O04+KsAjsxtkM+ybDV83iCUxes0ydQdalEGP1zK4mQ7ZtaZBsBc8Lmd6yyW+I7RXz4Hq3E2L3HY9m3Jw3ZQ7zH0Mypuwi/3/bfbxwC5Q4lo1gF5FS2yK9NsQndl102J5bPWftObh9pKuuxmM3+TRZ44pl/1tsIRwOLrMmlIxmtFk2eCh8RHCetHmZoRQDZ3fg9bfD1XdWdAGYxeF5UC5kYQshaEswltX0fShsRA0ZY+VoJYowotgfmUuyWT9OQ3sRNA3UOwC94lIN1mnNVHcWP2NQ06XMa33eLxrSRTOUsYcL0C+6tYCD4MGu49jrnBsQXDc9GZMtSO7JjROGg==",
            },
        )
        print(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 2)

    def test_users_register_failed_username_duplication(self):

        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        response = self.client.post(
            reverse("user-register"),
            data={
                "email": "Alice@gmail.com",
                "username": "publisher",
                "password_encrypted": "aNE7O04+KsAjsxtkM+ybDV83iCUxes0ydQdalEGP1zK4mQ7ZtaZBsBc8Lmd6yyW+I7RXz4Hq3E2L3HY9m3Jw3ZQ7zH0Mypuwi/3/bfbxwC5Q4lo1gF5FS2yK9NsQndl102J5bPWftObh9pKuuxmM3+TRZ44pl/1tsIRwOLrMmlIxmtFk2eCh8RHCetHmZoRQDZ3fg9bfD1XdWdAGYxeF5UC5kYQshaEswltX0fShsRA0ZY+VoJYowotgfmUuyWT9OQ3sRNA3UOwC94lIN1mnNVHcWP2NQ06XMa33eLxrSRTOUsYcL0C+6tYCD4MGu49jrnBsQXDc9GZMtSO7JjROGg==",
            },
        )

        print(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 2)

    def test_users_login_success(self):

        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
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

        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        response = self.client.post(
            reverse("user-login"),
            data={
                "email": "56@qq.com",
                "password_encrypted": "aNE7O04+KsAjsxtkM+ybDV83iCUxes0ydQdalEGP1zK4mQ7ZtaZBsBc8Lmd6yyW+I7RXz4Hq3E2L3HY9m3Jw3ZQ7zH0Mypuwi/3/bfbxwC5Q4lo1gF5FS2yK9NsQndl102J5bPWftObh9pKuuxmM3+TRZ44pl/1tsIRwOLrMmlIxmtFk2eCh8RHCetHmZoRQDZ3fg9bfD1XdWdAGYxeF5UC5kYQshaEswltX0fShsRA0ZY+VoJYowotgfmUuyWT9OQ3sRNA3UOwC94lIN1mnNVHcWP2NQ06XMa33eLxrSRTOUsYcL0C+6tYCD4MGu49jrnBsQXDc9GZMtSO7JjROGg==",
            },
        )
        print(response.content)
        self.assertEqual(response.status_code, 400)

    def test_users_login_failed_wrong_password(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        response = self.client.post(
            reverse("user-login"),
            data={
                "email": "123456@qq.com",
                "password_encrypted": "bdOG6lj/+APy6ZlBHjHyQWSqnzWI29UtsAfQPqaJbEWUypEf9lqOFmk1yLKuyds6KmosaKP6PsrKJIa9U1WtVDBhpRMbP+CkS2kNGHF72VQhRfnm1cMnWsSEgrolIGi3FZ+G6hf2Y+NL12kf9RRCRhLqtwWa6hQf7WSNBXQGJ1pktlUNY/Hry3J/kCgSEDZYJHO5bakJFKwQ+hIwuhFbtKsf0th1rTqhojlzJTfwd9nV7OEyQDgSVQ5U5MKSyH2DfsbjVMp5BIEJ1JCq+8uHDyhbawmZdC8JRfj+klwejSWcO8Z95ZISlIvbdkgypPO4Xlboovh0nIGMJmtFkGC5Og==",
            },
        )
        print(response.content)
        self.assertEqual(response.status_code, 400)

    def test_users_profile_detail_success(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))

        # --login
        publisher = User.objects.get(username="publisher")
        self.client.force_authenticate(user=publisher)

        # --profileTODO:有点问题？
        response = self.client.get(reverse("user-profile"))
        self.assertEqual(response.status_code, 200)

    def test_users_profile_detail_failed_not_login(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        response = self.client.get(reverse("user-profile"))
        self.assertEqual(response.status_code, 401)

    def test_users_profile_update_avatar_success_jpg(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        image = SimpleUploadedFile(
            name="test_image_jpg.jpg",
            content=b"fake image content",
            content_type="image/jpeg",
        )
        publisher = User.objects.get(username="publisher")
        self.client.force_authenticate(user=publisher)
        response = self.client.post(reverse("avatar-upload"), {"avatar": image})
        self.assertEqual(response.status_code, 200)
        self.assertIn("avatar", response.json())
        print(response.json()["avatar"])

    def test_users_profile_update_avatar_success_png(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        image = SimpleUploadedFile(
            name="test_image_png.png",
            content=b"fake image content",
            content_type="image/png",
        )
        publisher = User.objects.get(username="publisher")
        self.client.force_authenticate(user=publisher)
        response = self.client.post(reverse("avatar-upload"), {"avatar": image})
        self.assertEqual(response.status_code, 200)
        self.assertIn("avatar", response.json())
        print(response.json()["avatar"])

    def test_users_profile_update_avatar_success_gif(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        image = SimpleUploadedFile(
            name="test_image_gif.gif",
            content=b"fake image content",
            content_type="image/gif",
        )
        publisher = User.objects.get(username="publisher")
        self.client.force_authenticate(user=publisher)
        response = self.client.post(reverse("avatar-upload"), {"avatar": image})
        self.assertEqual(response.status_code, 200)
        self.assertIn("avatar", response.json())
        print(response.json()["avatar"])

    def test_users_profile_update_avatar_failed_not_login(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        image = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"fake image content",
            content_type="image/jpeg",
        )

        response = self.client.post(reverse("avatar-upload"), {"avatar": image})
        self.assertEqual(response.status_code, 401)

    def test_users_profile_update_avatar_failed_without_image(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))

        publisher = User.objects.get(username="publisher")
        self.client.force_authenticate(user=publisher)
        response = self.client.post(reverse("avatar-upload"))
        self.assertEqual(response.status_code, 400)

    def test_users_profile_update_avatar_failed_not_image(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        image = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"fake image content",
            content_type="application/pdf",
        )
        publisher = User.objects.get(username="publisher")
        self.client.force_authenticate(user=publisher)
        response = self.client.post(reverse("avatar-upload"), {"avatar": image})
        self.assertEqual(response.status_code, 400)

    def test_users_profile_edit_success_username(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        publisher = User.objects.get(username="publisher")
        self.client.force_authenticate(user=publisher)
        response = self.client.post(
            reverse("user-profile-edit"), {"username": "new_publisher"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "new_publisher")

    def test_users_profile_edit_success_email(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        publisher = User.objects.get(username="publisher")
        self.client.force_authenticate(user=publisher)
        response = self.client.post(
            reverse("user-profile-edit"), {"email": "newemail@qq.com"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], "newemail@qq.com")

    def test_users_profile_edit_success_password(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        publisher = User.objects.get(username="publisher")
        self.client.force_authenticate(user=publisher)
        response = self.client.post(
            reverse("user-profile-edit"),
            {
                "old_password_encrypted": "aNE7O04+KsAjsxtkM+ybDV83iCUxes0ydQdalEGP1zK4mQ7ZtaZBsBc8Lmd6yyW+I7RXz4Hq3E2L3HY9m3Jw3ZQ7zH0Mypuwi/3/bfbxwC5Q4lo1gF5FS2yK9NsQndl102J5bPWftObh9pKuuxmM3+TRZ44pl/1tsIRwOLrMmlIxmtFk2eCh8RHCetHmZoRQDZ3fg9bfD1XdWdAGYxeF5UC5kYQshaEswltX0fShsRA0ZY+VoJYowotgfmUuyWT9OQ3sRNA3UOwC94lIN1mnNVHcWP2NQ06XMa33eLxrSRTOUsYcL0C+6tYCD4MGu49jrnBsQXDc9GZMtSO7JjROGg==",
                "new_password_encrypted": "M/tiC/wdfvdIpLDhMJ/237g18ur+hOnvt4gux6tD+Ua1fIBp1f2BdSJM1gbih8WK6gxHBCvHAphR1ZzgmOX/kQGE2ubq3c1RwmJJ3HvebQQnXN8dfVQLA3PGv/4Mr4kUa2WKau/O/6jpRiY7BRwjMXFUv5B7n1leKoTiiFQlF9T4dE6QI7RIaovYap7xq6Or85a3SKI7VMKoHHSr2JuYwI9P2BqtTGP3MUZB/eRA2sIgmcnyXwNJfwv6zjBsTAg2UukNHKqvh/eRNYXLp4h9BSMRTgdSo1p0ogOIar3BHlVQHLpuZfnYgjdKH+5O9zsQosUVqieJjrMYNOBscGALjg==",
            },
        )
        self.assertEqual(response.status_code, 200)
        # 尝试新旧密码登录
        # old
        response = self.client.post(
            reverse("user-login"),
            data={
                "email": "123456@qq.com",
                "password_encrypted": "aNE7O04+KsAjsxtkM+ybDV83iCUxes0ydQdalEGP1zK4mQ7ZtaZBsBc8Lmd6yyW+I7RXz4Hq3E2L3HY9m3Jw3ZQ7zH0Mypuwi/3/bfbxwC5Q4lo1gF5FS2yK9NsQndl102J5bPWftObh9pKuuxmM3+TRZ44pl/1tsIRwOLrMmlIxmtFk2eCh8RHCetHmZoRQDZ3fg9bfD1XdWdAGYxeF5UC5kYQshaEswltX0fShsRA0ZY+VoJYowotgfmUuyWT9OQ3sRNA3UOwC94lIN1mnNVHcWP2NQ06XMa33eLxrSRTOUsYcL0C+6tYCD4MGu49jrnBsQXDc9GZMtSO7JjROGg==",
            },
        )
        self.assertEqual(response.status_code, 400)

        # new
        response = self.client.post(
            reverse("user-login"),
            data={
                "email": "123456@qq.com",
                "password_encrypted": "M/tiC/wdfvdIpLDhMJ/237g18ur+hOnvt4gux6tD+Ua1fIBp1f2BdSJM1gbih8WK6gxHBCvHAphR1ZzgmOX/kQGE2ubq3c1RwmJJ3HvebQQnXN8dfVQLA3PGv/4Mr4kUa2WKau/O/6jpRiY7BRwjMXFUv5B7n1leKoTiiFQlF9T4dE6QI7RIaovYap7xq6Or85a3SKI7VMKoHHSr2JuYwI9P2BqtTGP3MUZB/eRA2sIgmcnyXwNJfwv6zjBsTAg2UukNHKqvh/eRNYXLp4h9BSMRTgdSo1p0ogOIar3BHlVQHLpuZfnYgjdKH+5O9zsQosUVqieJjrMYNOBscGALjg==",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_users_profile_edit_failed_not_login(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        response = self.client.post(
            reverse("user-profile-edit"), {"username": "new_publisher"}
        )
        self.assertEqual(response.status_code, 401)

    def test_users_profile_edit_failed_password_wrong(self):
        print("\n\033[37;42m{}...\033[0m".format(inspect.currentframe().f_code.co_name))
        publisher = User.objects.get(username="publisher")
        self.client.force_authenticate(user=publisher)
        response = self.client.post(
            reverse("user-profile-edit"),
            {
                "old_password_encrypted": "M/tiC/wdfvdIpLDhMJ/237g18ur+hOnvt4gux6tD+Ua1fIBp1f2BdSJM1gbih8WK6gxHBCvHAphR1ZzgmOX/kQGE2ubq3c1RwmJJ3HvebQQnXN8dfVQLA3PGv/4Mr4kUa2WKau/O/6jpRiY7BRwjMXFUv5B7n1leKoTiiFQlF9T4dE6QI7RIaovYap7xq6Or85a3SKI7VMKoHHSr2JuYwI9P2BqtTGP3MUZB/eRA2sIgmcnyXwNJfwv6zjBsTAg2UukNHKqvh/eRNYXLp4h9BSMRTgdSo1p0ogOIar3BHlVQHLpuZfnYgjdKH+5O9zsQosUVqieJjrMYNOBscGALjg==",
                "new_password_encrypted": "aNE7O04+KsAjsxtkM+ybDV83iCUxes0ydQdalEGP1zK4mQ7ZtaZBsBc8Lmd6yyW+I7RXz4Hq3E2L3HY9m3Jw3ZQ7zH0Mypuwi/3/bfbxwC5Q4lo1gF5FS2yK9NsQndl102J5bPWftObh9pKuuxmM3+TRZ44pl/1tsIRwOLrMmlIxmtFk2eCh8RHCetHmZoRQDZ3fg9bfD1XdWdAGYxeF5UC5kYQshaEswltX0fShsRA0ZY+VoJYowotgfmUuyWT9OQ3sRNA3UOwC94lIN1mnNVHcWP2NQ06XMa33eLxrSRTOUsYcL0C+6tYCD4MGu49jrnBsQXDc9GZMtSO7JjROGg==",
            },
        )
        self.assertEqual(response.status_code, 400)
