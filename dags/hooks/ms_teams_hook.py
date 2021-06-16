# flake8: noqa
from airflow.exceptions import AirflowException
from airflow.hooks.http_hook import HttpHook


class MSTeamsWebhookHook(HttpHook):
    """
    This hook allows you to post messages to MS Teams using the Incoming Webhook connector.

    Takes both MS Teams webhook token directly and connection that has MS Teams webhook token.
    If both supplied, the webhook token will be appended to the host in the connection.

    :param http_conn_id: connection that has MS Teams webhook URL
    :type http_conn_id: str
    :param webhook_token: MS Teams webhook token
    :type webhook_token: str
    :param message: The message you want to send on MS Teams
    :type message: str
    :param subtitle: The subtitle of the message to send
    :type subtitle: str
    :param button_text: The text of the action button
    :type button_text: str
    :param button_url: The URL for the action button click
    :type button_url : str
    :param theme_color: Hex code of the card theme, without the #
    :type message: str
    :param proxy: Proxy to use when making the webhook request
    :type proxy: str

    """

    def __init__(
        self,
        http_conn_id=None,
        webhook_token=None,
        message="",
        subtitle="",
        button_text="",
        button_url="",
        theme_color="00FF00",
        image_url="",
        proxy=None,
        *args,
        **kwargs,
    ):
        super(MSTeamsWebhookHook, self).__init__(*args, **kwargs)
        self.http_conn_id = http_conn_id
        self.webhook_token = self.get_token(webhook_token, http_conn_id)
        self.message = message
        self.subtitle = subtitle
        self.button_text = button_text
        self.button_url = button_url
        self.theme_color = theme_color
        self.image_url = image_url
        self.proxy = proxy

    def get_proxy(self, http_conn_id):
        conn = self.get_connection(http_conn_id)
        extra = conn.extra_dejson
        print(extra)
        return extra.get("proxy", "")

    def get_token(self, token, http_conn_id):
        """
        Given either a manually set token or a conn_id, return the webhook_token to use
        :param token: The manually provided token
        :param conn_id: The conn_id provided
        :return: webhook_token (str) to use
        """
        if token:
            return token
        elif http_conn_id:
            conn = self.get_connection(http_conn_id)
            extra = conn.extra_dejson
            return extra.get("webhook_token", "")
        else:
            raise AirflowException(
                "Cannot get URL: No valid MS Teams " "webhook URL nor conn_id supplied"
            )

    def build_message(self):
        cardjson = """
                {{
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "{3}",
            "summary": "{0}",
            "sections": [{{
                "activityTitle": "{1}",
                "activitySubtitle": "{2}",
                "activityImage": "{6}",
                "markdown": true,
                "potentialAction": [
                    {{
                        "@type": "OpenUri",
                        "name": "{4}",
                        "targets": [
                            {{ "os": "default", "uri": "{5}" }}
                        ]
                    }}
                ]
            }}]
            }}
                """
        return cardjson.format(
            self.message,
            self.message,
            self.subtitle,
            self.theme_color,
            self.button_text,
            self.button_url,
            self.image_url,
        )

    def execute(self):
        """
        Remote Popen (actually execute the webhook call)

        :param cmd: command to remotely execute
        :param kwargs: extra arguments to Popen (see subprocess.Popen)
        """
        proxies = {}
        proxy_url = self.get_proxy(self.http_conn_id)
        print("Proxy is : " + proxy_url)
        if len(proxy_url) > 5:
            proxies = {"https": proxy_url}

        self.run(
            endpoint=self.webhook_token,
            data=self.build_message(),
            headers={"Content-type": "application/json"},
            extra_options={"proxies": proxies},
        )


def on_failure(context):
    SIREN_IMAGE = "https://trello-attachments.s3.amazonaws.com/602bccd86987e40ad661d398/128x128/5c70ea08f5d0a41ae2fc947919a33b12/siren.png"
    dag_id = context["task_instance"].dag_id
    task_id = context["task_instance"].task_id

    teams_notification_hook = MSTeamsWebhookHook(
        http_conn_id="msteams_webhook_url",
        message=f"# **Task Failed**\n\nTask: {task_id}\n\nDag: {dag_id}",
        button_text="Show Logs",
        button_url=context["task_instance"].log_url,
        theme_color="FF0000",
        image_url=SIREN_IMAGE,
    )
    teams_notification_hook.execute()
