from vk_api.utils import get_random_id
from vk_api import VkUpload
import varenv

def default_message(vk, user_id, text=None, attachment=None):
    if attachment == None:
        vk.messages.send(
            user_id=user_id,
            random_id=get_random_id(),
            message=text
        )
    elif text == None:
        vk.messages.send(
            user_id=user_id,
            random_id=get_random_id(),
            attachment=attachment
        )
    else:
        vk.messages.send(
            user_id=user_id,
            random_id=get_random_id(),
            message=text,
            attachment=attachment
        )

    return True

def keyboard_message(vk, user_id, text=None, keyboard=None, attachment=None):
    if attachment == None:
        vk.messages.send(
            user_id=user_id,
            random_id=get_random_id(),
            keyboard=keyboard,
            message=text
        )
    elif text == None:
        vk.messages.send(
            user_id=user_id,
            random_id=get_random_id(),
            keyboard=keyboard,
            attachment=attachment
        )
    else:
        vk.messages.send(
            user_id=user_id,
            random_id=get_random_id(),
            message=text,
            keyboard=keyboard,
            attachment=attachment
        )

    return True

def photo_upload(vk, photo, group_id=varenv.GROUP_ID):
    upload = VkUpload(vk)
    result = upload.photo_messages(photo, peer_id=0)
    photo_id = result[0]['id']
    return f'photo-{group_id}_{photo_id}'
