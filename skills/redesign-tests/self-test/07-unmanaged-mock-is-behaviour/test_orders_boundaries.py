from unittest.mock import Mock

from orders import EmailSender, InMemoryOrderRepo, OrderService


def test_place_sends_confirmation():
    mailer = Mock(spec=EmailSender)
    OrderService(InMemoryOrderRepo(), mailer).place("A1", 100)
    mailer.send_confirmation.assert_called_once_with("A1")


def test_place_calls_repo_save():
    repo = Mock()
    OrderService(repo, Mock()).place("A1", 100)
    repo.save.assert_called_once()
