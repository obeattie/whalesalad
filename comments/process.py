"""Processes the comments through filters."""
# This script will work when Django Ticket #7387 is fixed.
# TODO: Enable this script
import optparse, os, sys

sys.path = ['/Django/Source', '/usr/local/', ] + sys.path

from whalesalad import settings
from django.core.management import setup_environ

setup_environ(settings)

def get_unprocessed_objects(verbose=False):
    from whalesalad.comments.models import Comment
    objs = Comment.objects.filter(processed=False)
    if verbose:
        print 'Retrieved %i unprocessed objects from the database.' % objs.count()
    return objs

def process_objects(objects, verbose=False):
    if verbose:
        print 'Starting spam processing...'
    processed_count = 0
    for obj in objects:
        obj.Moderator(obj).process()
        if verbose:
            print 'Processed comment with ID #%i successfully.' % obj.id
        processed_count += 1
    if verbose:
        print 'Successfully processed all %i comments. Exiting.' % processed_count
    return processed_count

def run(verbose):
    return process_objects(objects=get_unprocessed_objects(verbose=verbose), verbose=verbose)

if __name__ == '__main__':
    # Script use
    option_parser = optparse.OptionParser()
    option_parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False, help='print status messages to stdout')
    (options, args) = option_parser.parse_args()
    
    run(verbose=options.verbose)
