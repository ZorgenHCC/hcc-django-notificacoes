import json

import requests


class Notification:
    def __init__(self, user, password, url_host):
        """
        :param str user: Superuser's username
        :param str password: Superuser's password
        :param str url_host: Microservice's base url e.g. http://localhost:8765
        """
        self.user = user
        self.password = password
        self.url_host = url_host
        self.__token = self.__get_token()

    def __get_token(self) -> str:
        """
        Get token to use in requests to notifications microservice

        :return: Token for microservice
        :rtype: str

        """
        data = ''
        r = requests.post(
            f'{self.url_host}/auth',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({'username': self.user, 'password': self.password})
        )
        if r.status_code == 200:
            data = f'Token {r.json()["token"]}'
        return data

    def get_notifications(self, user_email: str = '', context: str = '', limit: int = 10, offset: int = 0) -> dict:
        """
        Get notifications from microservice, it can be filtered or not.

        :param user_email: User_email used to create a notification
        :param context: Context used to create a notification
        :param limit: Return a limited number of notifications
        :param offset: Used to set the initial number of notifications' index list
        :return: Notifications found with pagination configuration
        :raises Exception: If some error ocurred
        """
        data = {}
        url = f'{self.url_host}/notification?limit={limit}&offset={offset}&read=False'
        if user_email:
            url += f'&user_email={user_email}'
        if context:
            url += f'&context={context}'
        try:
            r = requests.get(url, headers={'Authorization': self.__token})
            if r.status_code == 200:
                data = r.json()
        except Exception as e:
            return {
                'error_msg': f'{e}',
                'message': 'Não foi possível buscar notificações, tente novamente'
            }
        return data

    def create_notification(self, users_email: list = [], text: str = '', context: str = '', redirect_url: str = '',
                            franchises: list = [], identifier: str = '') -> str:
        """
        Create a notification in microservice

        :param users_email: Users_email's list
        :param text: Notification's text
        :param context: Notification's context
        :param redirect_url: Notification's redirect URL
        :param franchises: Notification's franchise list
        :param identifier: Notification's identifier
        :return: A string is returned to show creation success
        :rtype: str
        :raises Exception: If some error ocurred
        """

        data = {}

        if users_email:
            data.update({'users_email': users_email})
        if text:
            data.update({'text': text})
        if context:
            data.update({'context': context})
        if redirect_url:
            data.update({'redirect_url': redirect_url})
        if franchises:
            data.update({'franchises': franchises})
        if identifier:
            data.update({'identifier': identifier})

        try:
            r = requests.post(
                f'{self.url_host}/notification',
                headers={
                    'Authorization': self.__token,
                    'Content-Type': 'application/json'
                },
                data=json.dumps(data)
            )

            if r.status_code == 200:
                return r.json()
            else:
                raise Exception

        except Exception as e:
            return 'Não foi possível criar notificações, tente novamente'

    def update_notification(self, notification_id: str = '', read: bool = False, opened: bool = False) -> str:
        """
        Update read and opened notification's values.

        :param notification_id: The id (uuid) of notification
        :param read: Attribute to set if a notification was read
        :param opened: Attribute to set if a notification was opened
        :return: The notification updated
        :rtype: dict
        """
        data = {}

        if read:
            data.update({"read": True})
        if opened:
            data.update({"opened": True})
        try:
            r = requests.patch(
                f'{self.url_host}/notification/{notification_id}',
                headers={
                    'Authorization': self.__token,
                    'Content-Type': 'application/json'
                },
                data=json.dumps(data)
            )

            if r.status_code == 200:
                return r.json()
            else:
                raise Exception

        except Exception as e:
            return 'Não foi possível atualizar a notificação, tente novamente'
