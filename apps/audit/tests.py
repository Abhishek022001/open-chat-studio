from unittest import mock

from field_audit.models import USER_TYPE_REQUEST

from apps.audit.auditors import AuditContextProvider
from apps.teams.utils import current_team


def test_change_context():
    request = AuthedRequest()
    assert AuditContextProvider().change_context(request) == {
        "user_type": USER_TYPE_REQUEST,
        "username": request.user.username,
    }


def test_change_context_returns_none_without_request():
    assert AuditContextProvider().change_context(None)["user_type"] != USER_TYPE_REQUEST


def test_change_context_returns_none_without_request_with_team():
    with current_team(AuthedRequest.Team()):
        context = AuditContextProvider().change_context(None)
        assert context["user_type"] != USER_TYPE_REQUEST
        assert context["team"] == 17


def test_change_context_returns_value_for_unauthorized_req():
    request = AuthedRequest(auth=False)
    assert AuditContextProvider().change_context(request) == {}


def test_change_context_returns_value_for_unauthorized_team_req():
    request = AuthedRequest(auth=False)
    with current_team(AuthedRequest.Team()):
        assert AuditContextProvider().change_context(request) == {"team": 17}


def test_change_context_returns_value_for_authorized_team_req():
    request = AuthedRequest(auth=True)
    with current_team(AuthedRequest.Team()):
        assert AuditContextProvider().change_context(request) == {
            "user_type": USER_TYPE_REQUEST,
            "username": "test@example.com",
            "team": 17,
        }


@mock.patch("apps.audit.auditors._get_hijack_username", return_value="admin@example.com")
def test_change_context_hijacked_request(_):
    request = AuthedRequest(session={"hijack_history": [1]})
    assert AuditContextProvider().change_context(request) == {
        "user_type": USER_TYPE_REQUEST,
        "username": "admin@example.com",
        "as_username": request.user.username,
    }


@mock.patch("apps.audit.auditors._get_hijack_username", return_value=None)
def test_change_context_hijacked_request__no_hijacked_user(_):
    request = AuthedRequest(session={"hijack_history": [1]})
    assert AuditContextProvider().change_context(request) == {
        "user_type": USER_TYPE_REQUEST,
        "username": "test@example.com",
    }


def test_change_context_hijacked_request__bad_hijack_history():
    request = AuthedRequest(session={"hijack_history": ["not a number"]})
    assert AuditContextProvider().change_context(request) == {
        "user_type": USER_TYPE_REQUEST,
        "username": "test@example.com",
    }


class AuthedRequest:
    class User:
        username = "test@example.com"
        is_authenticated = True

    class Team:
        id = 17
        slug = "seventeen"

    def __init__(self, auth=True, session=None):
        self.user = self.User()
        self.session = session or {}
        self.user.is_authenticated = auth
