from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-c','--cont',nargs='?', const='c',default='hello')

        # parser.add_argument('-m', nargs='+',type=int,
                            # help='The current Django project folder name')
        # parser.add_argument('new', type=str, nargs='+',
                            # help='The new Django project name')
    
    def handle(self, *args, **options):
        print(args)
        for key, value in options.items():
            print(key,'----', value)
        # User = get_user_model()
        # if not User.objects.filter(username="admin").exists():
        #     User.objects.create_superuser(
        #         "admin", "admin@domain.com", "admin")
        #     self.stdout.write(self.style.SUCCESS('Admin user has created'))
        # else:
        #     self.stdout.write(self.style.SUCCESS('Admin user already exists'))


        self.stdout.write(self.style.SUCCESS('--------END---------'))
        
