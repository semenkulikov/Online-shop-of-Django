from authapp.models import User
from interfaces.profile_interface import ProfileInterface
from profileapp.models import Profile


class ProfileRepository(ProfileInterface):
    def get_profile(self, user: User) -> Profile:
        return Profile.objects.get(user=user)

    def get_profile_by_phone_number(self, phone_number):
        return Profile.objects.filter(phone_number=phone_number).first()
