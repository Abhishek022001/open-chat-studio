import pytest
from django.forms.widgets import HiddenInput, Select

from apps.channels.forms import ChannelForm, WhatsappChannelForm
from apps.channels.models import ChannelPlatform
from apps.service_providers.models import MessagingProvider, MessagingProviderType
from apps.utils.factories.service_provider_factories import MessagingProviderFactory


@pytest.mark.parametrize(
    ("platform", "expected_widget_cls"),
    [
        ("whatsapp", Select),
        ("telegram", HiddenInput),
    ],
)
def test_channel_form_reveals_provider_types(team_with_users, platform, expected_widget_cls):
    """Test that the message provider field is being hidden when not applicable to a certain platform"""
    # First create a messaging provider
    message_provider = MessagingProviderFactory(type=MessagingProviderType("twilio"), team=team_with_users)
    MessagingProviderFactory(type=MessagingProviderType("twilio"))

    form = ChannelForm(initial={"platform": ChannelPlatform(platform)}, team=team_with_users)
    widget = form.fields["messaging_provider"].widget
    assert isinstance(widget, expected_widget_cls)

    form_queryset = form.fields["messaging_provider"].queryset
    assert form_queryset.count() == MessagingProvider.objects.filter(team=team_with_users).count()
    assert form_queryset.first() == message_provider


@pytest.mark.parametrize(
    ("number", "is_valid"),
    [
        ("+27812345678", True),
        ("0812345678", False),
        ("+27 81 234 5678", True),
        ("+27-81-234-5678", True),
        ("+27-81 2345678", True),
        ("+27_81_234_5678", False),
        ("0800 100 030", False),
        ("+32 (0)27888484", True),
    ],
)
def test_whatsapp_form(number, is_valid):
    form = WhatsappChannelForm({"number": number})
    assert form.is_valid() == is_valid
    if not is_valid:
        assert form.errors["number"] == ["Enter a valid phone number (e.g. +12125552368)."]
