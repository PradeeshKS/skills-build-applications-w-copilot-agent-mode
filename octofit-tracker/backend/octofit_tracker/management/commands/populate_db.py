from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data (delete children first)
        Activity.objects.filter(pk__isnull=False).delete()
        Workout.objects.filter(pk__isnull=False).delete()
        Leaderboard.objects.filter(pk__isnull=False).delete()
        User.objects.filter(pk__isnull=False).delete()
        Team.objects.filter(pk__isnull=False).delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel', description='Marvel Superheroes')
        dc = Team.objects.create(name='DC', description='DC Superheroes')

        # Create users
        from bson import ObjectId
        user_objs = []
        users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': marvel, 'is_superhero': True},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': marvel, 'is_superhero': True},
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': marvel, 'is_superhero': True},
            {'name': 'Superman', 'email': 'superman@dc.com', 'team': dc, 'is_superhero': True},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': dc, 'is_superhero': True},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': dc, 'is_superhero': True},
        ]
        for user_data in users:
            user_data['id'] = ObjectId()
            user_obj = User.objects.create(**user_data)
            user_objs.append(user_obj)

        # Create activities
        for user in user_objs:
            Activity.objects.create(user=user, type='Running', duration=30)
            Activity.objects.create(user=user, type='Cycling', duration=45)

        # Create workouts
        cardio = Workout.objects.create(name='Cardio', description='Cardio workout')
        strength = Workout.objects.create(name='Strength', description='Strength workout')
        superhero_users = [u for u in user_objs if u.is_superhero]
        cardio.suggested_for.set(superhero_users)
        strength.suggested_for.set(superhero_users)

        # Create leaderboards
        Leaderboard.objects.create(team=marvel, points=150)
        Leaderboard.objects.create(team=dc, points=120)

        # Djongo will enforce unique email via model field
        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))
