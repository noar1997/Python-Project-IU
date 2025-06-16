import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from classes import can_complete_habit, streak_broken, Habits

class TestCanCompleteHabit(unittest.TestCase):
    def setUp(self):
        self.today = datetime(2025, 6, 15)

    def test_daily(self):
        yesterday = self.today - timedelta(days=1)
        same_day = self.today
        self.assertTrue(can_complete_habit({"frequency": "daily"}, yesterday, self.today))
        self.assertFalse(can_complete_habit({"frequency": "daily"}, same_day, self.today))

    def test_weekly(self):
        last_week = self.today - timedelta(days=7)
        not_enough = self.today - timedelta(days=5)
        self.assertTrue(can_complete_habit({"frequency": "weekly"}, last_week, self.today))
        self.assertFalse(can_complete_habit({"frequency": "weekly"}, not_enough, self.today))

    def test_monthly(self):
        last_month = datetime(2025, 5, 15)
        same_month = datetime(2025, 6, 1)
        self.assertTrue(can_complete_habit({"frequency": "monthly"}, last_month, self.today))
        self.assertFalse(can_complete_habit({"frequency": "monthly"}, same_month, self.today))

    def test_invalid_frequency(self):
        self.assertFalse(can_complete_habit({"frequency": "yearly"}, self.today, self.today))


class TestStreakBroken(unittest.TestCase):
    def setUp(self):
        self.today = datetime(2025, 6, 15)

    def test_daily(self):
        day_gap = self.today - timedelta(days=2)
        ok_gap = self.today - timedelta(days=1)
        self.assertTrue(streak_broken(day_gap, self.today, "daily"))
        self.assertFalse(streak_broken(ok_gap, self.today, "daily"))

    def test_weekly(self):
        too_long = self.today - timedelta(days=8)
        ok = self.today - timedelta(days=7)
        self.assertTrue(streak_broken(too_long, self.today, "weekly"))
        self.assertFalse(streak_broken(ok, self.today, "weekly"))

    def test_monthly(self):
        too_long = self.today - timedelta(days=32)
        ok = self.today - timedelta(days=30)
        self.assertTrue(streak_broken(too_long, self.today, "monthly"))
        self.assertFalse(streak_broken(ok, self.today, "monthly"))

    def test_invalid_frequency(self):
        self.assertFalse(streak_broken(self.today - timedelta(days=100), self.today, "yearly"))


class TestHabitCreation(unittest.TestCase):

    @patch("classes.save_credentials")
    @patch("classes.load_credentials")
    def test_create_own_habit(self, mock_load, mock_save):
        mock_data = {"user1": {"password": "pass123", "habits": []}}
        mock_load.return_value = mock_data

        habits = Habits()
        habits.create_own_habit("user1", "Read Books", "daily")

        self.assertEqual(len(mock_data["user1"]["habits"]), 1)
        added_habit = mock_data["user1"]["habits"][0]
        self.assertEqual(added_habit["habit"], "Read Books")
        self.assertEqual(added_habit["frequency"], "daily")
        self.assertEqual(added_habit["streak"], 0)
        self.assertEqual(added_habit["progress"], 0)

        mock_save.assert_called_once_with(mock_data)

    @patch("classes.save_credentials")
    @patch("classes.load_credentials")
    def test_add_predefined_habit(self, mock_load, mock_save):
        mock_data = {"user1": {"password": "pass123", "habits": []}}
        mock_load.return_value = mock_data

        habits = Habits()
        habits.add_predefined_habit("user1", "Exercise", "weekly")

        self.assertEqual(len(mock_data["user1"]["habits"]), 1)
        added_habit = mock_data["user1"]["habits"][0]
        self.assertEqual(added_habit["habit"], "Exercise")
        self.assertEqual(added_habit["frequency"], "weekly")
        self.assertEqual(added_habit["streak"], 0)
        self.assertEqual(added_habit["progress"], 0)

        mock_save.assert_called_once_with(mock_data)


if __name__ == "__main__":
    unittest.main()
