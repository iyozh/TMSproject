from django.contrib.auth import get_user_model

from applications.onboarding.models import Profile

User = get_user_model()


class CurrentUserMixin:
    def get_object(self, queryset=None):

        if self.request.user.is_anonymous:
            return None

        if not queryset:
            queryset = self.model.objects.all()
        queryset = queryset.filter(user=self.request.user)
        return queryset.first()

    def get_current_avatar(self):
        avatar = None
        exc_missing = (
            User.profile.RelatedObjectDoesNotExist,
            Profile.avatar.RelatedObjectDoesNotExist,
        )
        try:
            avatar = self.request.user.profile.avatar
        except exc_missing:
            pass
        return avatar
