import math
import re

from django.utils.html import strip_tags


def count_words(html_string):
    # html_string = """
    # <h1>This is a title</h1>
    # """
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    count = len(matching_words)  # joincfe.com/projects/
    return count


def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count/200.0)  # assuming 200wpm reading
    # read_time_sec = read_time_min * 60
    # read_time = str(datetime.timedelta(seconds=read_time_sec))
    # read_time = str(datetime.timedelta(minutes=read_time_min))
    return int(read_time_min)


def upload_location(instance, filename):
    if instance.id:
        return "post/{}/{}".format(instance.id, filename)

    model = instance.__class__
    last_obj = model.objects.order_by("id").last()

    if last_obj:
        new_id = last_obj.id + 1
    else:
        new_id = 1

    return "post/{}/{}".format(new_id, filename)