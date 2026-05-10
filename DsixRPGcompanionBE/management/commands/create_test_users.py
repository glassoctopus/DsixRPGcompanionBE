from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test users (superuser, staff, GM, regular user)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interactive',
            action='store_true',
            help='Ask for passwords interactively (otherwise uses defaults)',
        )

    def handle(self, *args, **options):
        interactive = options['interactive']
        
        # 1. Superuser
        if not User.objects.filter(username='superadmin').exists():
            if interactive:
                password = input('Password for superadmin: ')
            else:
                password = 'supersecret123'
            superuser = User.objects.create_superuser(
                username='superadmin',
                email='superadmin@example.com',
                password=password,
                first_name='Super',
                last_name='Admin',
                is_staff=True,
                is_superuser=True,
            )
            self.stdout.write(self.style.SUCCESS(f'Created superuser: {superuser.username}'))
        else:
            self.stdout.write('Superuser already exists, skipping...')

        # 2. Staff user (admin)
        if not User.objects.filter(username='staffuser').exists():
            if interactive:
                password = input('Password for staffuser: ')
            else:
                password = 'staffpass123'
            staff_user = User.objects.create_user(
                username='staffuser',
                email='staff@example.com',
                password=password,
                first_name='Staff',
                last_name='User',
                is_staff=True,
                is_superuser=False,
            )
            self.stdout.write(self.style.SUCCESS(f'Created staff user: {staff_user.username}'))
        else:
            self.stdout.write('Staff user already exists, skipping...')

        # 3. Game Master (GM)
        if not User.objects.filter(username='gmuser').exists():
            if interactive:
                password = input('Password for gmuser: ')
            else:
                password = 'gmpass123'
            gm_user = User.objects.create_user(
                username='gmuser',
                email='gm@example.com',
                password=password,
                first_name='Game',
                last_name='Master',
                is_staff=False,
                is_superuser=False,
                game_master=True,
                game_master_approved=True,
                game_master_requested_at=timezone.now(),
            )
            # implement GM request here after I create functionality. 
            self.stdout.write(self.style.SUCCESS(f'Created GM user: {gm_user.username}'))
        else:
            self.stdout.write('GM user already exists, skipping...')

        # 4. Regular user
        if not User.objects.filter(username='regularuser').exists():
            if interactive:
                password = input('Password for regularuser: ')
            else:
                password = 'userpass123'
            regular_user = User.objects.create_user(
                username='regularuser',
                email='regular@example.com',
                password=password,
                first_name='Regular',
                last_name='User',
                is_staff=False,
                is_superuser=False,
                game_master=False,
                game_master_approved=False,
            )
            self.stdout.write(self.style.SUCCESS(f'Created regular user: {regular_user.username}'))
        else:
            self.stdout.write('Regular user already exists, skipping...')

        self.stdout.write(self.style.SUCCESS('All test users created/verified successfully!'))