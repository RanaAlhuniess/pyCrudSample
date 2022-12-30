from django.contrib.auth.tokens import PasswordResetTokenGenerator  
from datetime import datetime

class TokenGenerator(PasswordResetTokenGenerator):  
    def make_token(self, user):
        """
        Return a token that can be used once to do a password reset
        for the given user.
        """
        return self._make_token_with_timestamp(
            user,
            self._num_seconds(self._now()),
            self.secret,
        )

    def _num_seconds(self, dt):
        return int((dt - datetime(2001, 1, 1)).total_seconds())


account_token_generator = TokenGenerator()  