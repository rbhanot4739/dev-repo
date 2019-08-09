from django.core.management import BaseCommand
from posts.models import Post


class Command(BaseCommand):
    help = 'Creates the posts in the posts table'

    def handle(self, *args, **options):
        posts = []
        for i in range(20):
            p = Post(title=f'Post {i}', content=f'\nPost {i}'* 100)
            posts.append(p)
        Post.objects.bulk_create(posts)
        self.stdout.write(self.style.SUCCESS('Successfully created posts'))
