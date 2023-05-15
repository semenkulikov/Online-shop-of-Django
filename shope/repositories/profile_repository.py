from authapp.models import User
from interfaces.profile_interface import ProfileInterface
from profileapp.models import Profile


class ProfileRepository(ProfileInterface):
    def get_profile(self, user: User) -> Profile:
        return Profile.objects.get(user=user)
