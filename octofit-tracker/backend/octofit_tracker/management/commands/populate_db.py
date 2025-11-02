from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel', description='Marvel Superheroes')
        dc = Team.objects.create(name='DC', description='DC Superheroes')

        # Create users
        users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': marvel, 'is_superhero': True},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': marvel, 'is_superhero': True},
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': marvel, 'is_superhero': True},
            {'name': 'Superman', 'email': 'superman@dc.com', 'team': dc, 'is_superhero': True},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': dc, 'is_superhero': True},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': dc, 'is_superhero': True},
        ]
        for user_data in users:
            User(**user_data).save()

        # Create activities
        for user in User.objects.all():
            Activity.objects.create(user=user, type='Running', duration=30)
            Activity.objects.create(user=user, type='Cycling', duration=45)

        # Create workouts
        cardio = Workout.objects.create(name='Cardio', description='Cardio workout')
        strength = Workout.objects.create(name='Strength', description='Strength workout')
        cardio.suggested_for.set(User.objects.filter(is_superhero=True))
        strength.suggested_for.set(User.objects.filter(is_superhero=True))

        # Create leaderboards
        Leaderboard.objects.create(team=marvel, points=150)
        Leaderboard.objects.create(team=dc, points=120)

        # Ensure unique index on email field in users collection
        with connection.cursor() as cursor:
            cursor.execute('''db.users.createIndex({ "email": 1 }, { "unique": true })''')

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))
