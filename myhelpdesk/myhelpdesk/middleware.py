from datetime import datetime, timedelta

from user.views import logout_user


class UserLogout:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and not request.user.is_staff:
            user_id = request.user.id
            last_activity_str = request.session.get('last_activity')
            if last_activity_str:
                last_activity = datetime.strptime(last_activity_str, '%Y-%m-%d %H:%M:%S.%f')
                if (datetime.now() - last_activity) > timedelta(minutes=1):
                    logout_user(request)
            request.session['last_activity'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        return response
