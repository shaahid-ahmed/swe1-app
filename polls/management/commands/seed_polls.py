from django.core.management.base import BaseCommand
from django.utils import timezone

from polls.models import Question

POLLS = {
    "How would you rate this course overall?": [
        "Excellent",
        "Good",
        "Average",
        "Needs improvement",
    ],
    "How is the pace of the class?": ["Too slow", "Just right", "Too fast"],
    "Which part of the course is most useful so far?": [
        "Lectures",
        "Labs / hands-on work",
        "Group project",
        "Readings",
    ],
    "How clear are the assignment instructions?": [
        "Very clear",
        "Mostly clear",
        "Confusing",
    ],
    "What should we spend more time on?": [
        "Design and architecture",
        "Testing",
        "Cloud deployment",
        "Team collaboration",
    ],
    "How well is your team communicating?": ["Excellent", "Good", "Needs work", "Poor"],
    "How is the workload split in your team?": [
        "Very fair",
        "Mostly fair",
        "Uneven",
        "One or two people do most of it",
    ],
    "How confident are you that the project will be finished on time?": [
        "Very confident",
        "Somewhat confident",
        "Unsure",
        "Not confident",
    ],
    "What is your team's biggest challenge right now?": [
        "Time management",
        "Technical difficulties",
        "Unclear requirements",
        "Coordination",
    ],
    "How useful are the team meetings?": [
        "Very useful",
        "Somewhat useful",
        "Not very useful",
    ],
    "Which tool helps your team the most?": [
        "GitHub",
        "Slack / chat",
        "Project board",
        "Shared docs",
    ],
}


class Command(BaseCommand):
    help = "Create the sample feedback polls if there are no questions yet."

    def handle(self, *args, **options):
        if Question.objects.exists():
            self.stdout.write("Polls already exist, skipping.")
            return
        for text, choices in POLLS.items():
            question = Question.objects.create(
                question_text=text, pub_date=timezone.now()
            )
            for choice in choices:
                question.choice_set.create(choice_text=choice)
        self.stdout.write(f"Created {len(POLLS)} polls.")
