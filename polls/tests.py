import datetime
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


def make_question(text, days=0):
    pub_date = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=text, pub_date=pub_date)


class QuestionModelTests(TestCase):
    def test_recent_question(self):
        self.assertTrue(make_question("Recent").was_published_recently())

    def test_old_question(self):
        self.assertFalse(make_question("Old", days=-2).was_published_recently())

    def test_str(self):
        self.assertEqual(str(make_question("Hello?")), "Hello?")


class PollViewTests(TestCase):
    def test_index_empty(self):
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")

    def test_index_lists_question(self):
        make_question("What's up?")
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "What&#x27;s up?")

    def test_detail_and_results(self):
        q = make_question("Q")
        q.choice_set.create(choice_text="A")
        self.assertContains(self.client.get(reverse("polls:detail", args=(q.id,))), "A")
        self.assertEqual(
            self.client.get(reverse("polls:results", args=(q.id,))).status_code, 200
        )

    def test_missing_question_404(self):
        self.assertEqual(
            self.client.get(reverse("polls:detail", args=(99,))).status_code, 404
        )

    def test_vote(self):
        q = make_question("Q")
        c = q.choice_set.create(choice_text="A")
        response = self.client.post(
            reverse("polls:vote", args=(q.id,)), {"choice": c.id}
        )
        self.assertRedirects(response, reverse("polls:results", args=(q.id,)))
        c.refresh_from_db()
        self.assertEqual(c.votes, 1)

    def test_vote_without_choice(self):
        q = make_question("Q")
        response = self.client.post(reverse("polls:vote", args=(q.id,)))
        self.assertContains(response, "You didn&#x27;t select a choice.")


class SeedPollsTests(TestCase):
    def test_seed_creates_polls_once(self):
        call_command("seed_polls", stdout=StringIO())
        count = Question.objects.count()
        self.assertGreater(count, 0)
        call_command("seed_polls", stdout=StringIO())
        self.assertEqual(Question.objects.count(), count)
