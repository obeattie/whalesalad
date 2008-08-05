""" Script for conversion of a Wordpress database to the new Django schema.
    Converts blog posts, categories, tags and comments. I think that should cover
    everything.
    
    By Oliver Beattie. """

# Wordpress DB Config -- SET THESE!
WP_DB_NAME = ''
WP_DB_USER = ''
WP_DB_PASS = ''
WP_DB_HOST = 'localhost'

# --- DON'T MODIFY ME! --- 

# Setup for Django (as this is a script)
import MySQLdb, pytz, sys
from MySQLdb import cursors as sql_cursors
if not '/usr/local' in sys.path:
    sys.path = [ '/usr/local' ] + sys.path

from whalesalad import settings # Assumed to be on Python path
from django.core.management import setup_environ
setup_environ(settings)

from django.conf import settings

# All set-up
wp_cursor = MySQLdb.connect(
    host=WP_DB_HOST,
    user=WP_DB_USER,
    passwd=WP_DB_PASS,
    db=WP_DB_NAME,
    cursorclass=sql_cursors.DictCursor,
    use_unicode=True,
    charset='utf8'
).cursor()

# Import models
from django.contrib.auth.models import User
from whalesalad.blog.models import Post, PostTag
from whalesalad.metadata.models import Category

superuser = User.objects.filter(is_superuser=True)[0]

def localize_dt(dt):
    """Converts a UTC datetime into the correct timestamp for the
       current locale. Actually returns a naive datetime, as of a Django
       bug not handling aware datetimes properly with MySQL."""
    return pytz.utc.localize(dt).astimezone(pytz.timezone(settings.TIME_ZONE)).replace(tzinfo=None)

# Wordpress Terms Migration
def migrate_tags(wp_post_id, django_post_obj):
    """Migrates tags from the Wordpress taxonomy tables to PostTags."""
    # One ugly query
    wp_cursor.execute('SELECT `wp_terms`.`name` FROM `wp_posts` LEFT OUTER JOIN `wp_term_relationships` ON `wp_term_relationships`.`object_id` = `wp_posts`.`ID` INNER JOIN `wp_term_taxonomy` ON `wp_term_taxonomy`.`term_taxonomy_id` = `wp_term_relationships`.`term_taxonomy_id` INNER JOIN `wp_terms` ON `wp_terms`.`term_id` = `wp_term_taxonomy`.`term_id` WHERE `wp_term_taxonomy`.`taxonomy` = \'post_tag\' AND `wp_posts`.`ID` = %i;' % wp_post_id)
    for tag in wp_cursor.fetchall():
        # If the tag name contains spaces, then it needs to be quoted before being passed to
        # parse_tag_input (in generic.tagging.utils)
        tag_name = tag['name']
        if len(tag_name.split(' ')) > 1:
            tag_name = '"%s"' % tag_name
        # Append this to the existing list of tags
        django_post_obj.tags = '%s %s' % (django_post_obj.tags, tag_name)
    django_post_obj.save()

def migrate_categories(wp_post_id, django_post_obj):
    """Migrates tags from the Wordpress taxonomy tables to our Category model."""
    # Another goddamn ugly query...
    wp_cursor.execute('SELECT `wp_terms`.`name`, `wp_terms`.`slug` FROM `wp_posts` LEFT OUTER JOIN `wp_term_relationships` ON `wp_term_relationships`.`object_id` = `wp_posts`.`ID` INNER JOIN `wp_term_taxonomy` ON `wp_term_taxonomy`.`term_taxonomy_id` = `wp_term_relationships`.`term_taxonomy_id` INNER JOIN `wp_terms` ON `wp_terms`.`term_id` = `wp_term_taxonomy`.`term_id` WHERE `wp_term_taxonomy`.`taxonomy` = \'category\' AND `wp_posts`.`ID` = %i;' % wp_post_id)
    for cat in wp_cursor.fetchall():
        category = Category.objects.get_or_create(name=cat['name'], slug=cat['slug'])[0]
        django_post_obj.categories.add(category)
        django_post_obj.save()

def check_slug(slug):
    slug = slug[:50]
    if not Post.objects.filter(slug__exact=slug).count() > 0:
        return slug
    else:
        slug = slug[:48]
        counter = 1
        unique = False
        reformed_slug_base = '%s-' % slug
        reformed_slug = '%s%i' % (reformed_slug_base, counter)
        while not unique:
            if not Post.objects.filter(slug__exact=reformed_slug).count() > 0:
                unique = True
                break
            counter += 1
            reformed_slug = '%s%i' % (reformed_slug_base, counter)
        return reformed_slug

def migrate_posts():
    """Migrates all of the posts from Wordpress to Django."""
    wp_cursor.execute('SELECT * FROM `wp_posts` WHERE `post_type` = \'post\' AND `post_status` = \'publish\';')
    for post in wp_cursor.fetchall():
        # Iterate over every post
        content = post['post_content'].split('<!--more-->')
        print content
        if len(content) < 2:
            content.append(u'')
        elif len(content) > 2:
            content = [content[0], u''.join(content[1:])]
        post_obj = Post.objects.create(
            title=post['post_title'],
            slug=check_slug(post['post_name'])[:50],
            published=localize_dt(post['post_date_gmt']),
            author=superuser,
            is_public=True,
            intro=content[0],
            body=content[1]
        )
        # Migrate metadata
        migrate_tags(post['ID'], post_obj)
        migrate_categories(post['ID'], post_obj)
        print post_obj
