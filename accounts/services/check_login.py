from accounts.models import CustomUser


class CheckLogin:
    def __init__(self, user):
        self.email = user.email
        self.password = user.password

    def check_login(self):
        try:
            user = CustomUser.objects.get(email=self.email)
            if user.check_password(self.password):
                return user
        except CustomUser.DoesNotExist:
            return None
        return None