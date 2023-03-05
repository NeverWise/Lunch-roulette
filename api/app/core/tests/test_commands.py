"""
Test custom Django management commands.
"""

# Due possibili eccezioni che si possono ottenere.
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError

from unittest.mock import patch
from django.core.management import call_command
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    # Si imposta il risultato del metodo check uguale a True e ci si
    # aspetta che venga chiamato una sola volta.
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    # Si impostano una serie di eccezioni come risultato del metodo check
    # e ci si aspetta che venga chiamato 6 volte.
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
