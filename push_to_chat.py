from os import path

import argparse
import logging
import os
import sys

from rocketchat_API.rocketchat import RocketChat

#------------------------------------------------------------------------------
# Main script
#------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Add messages and files to chat')
parser.add_argument('--post_messages',
    action='store_true',
    help='Read file and place content to chat instead of file upload',
)
parser.add_argument('file',
    type=str,
    help='File to use',
)
args = parser.parse_args()

script_path = os.path.dirname(os.path.realpath(__file__))
log_path = path.join(script_path, 'ords_push_chat.log')
if path.isfile(log_path):
    os.remove(log_path)

logging.basicConfig(filename=log_path, format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')
l = logging.getLogger('ords.analysis')
l.setLevel(logging.DEBUG)

with open(path.join(script_path, '.rocketchat_user'), 'r') as f:
    rocketchat_user = f.readline().strip()

with open(path.join(script_path, '.rocketchat_token'), 'r') as f:
    rocketchat_token = f.readline().strip()

with open(path.join(script_path, '.rocketchat_url'), 'r') as f:
    rocketchat_url = f.readline().strip()

rocket = RocketChat(user=rocketchat_user, password=rocketchat_token, server_url=rocketchat_url)
room_id = rocket.rooms_info(room_name='ords').json()['room']['_id']

if args.post_messages:
    l.debug('Post messages from file "%s" to room "%s"' % (args.file, room_id))
    with open(path.join(script_path, args.file), 'r') as f:
        content = f.read()
        rocket.chat_post_message(content, room_id=room_id)
else:
    l.debug('Uploading file "%s" to room "%s"' % (args.file, room_id))
    l.debug(rocket.rooms_upload(room_id, args.file).json())
