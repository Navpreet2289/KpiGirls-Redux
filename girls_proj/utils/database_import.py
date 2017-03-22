import json

from django.core.files import File


with open('docs/parsed_db.json', encoding='utf-8') as data_file:
    data = json.load(data_file)

counter = 0
sum_lens = len(data)

for girl in data:
    try:
        local_file = open("docs/girls_photos/{}.jpg".format(girl['id']), 'rb')
    except OSError: # skipping import if file doesn't exist
        continue
    djangofile = File(local_file)
    if not girl['status']:
        status = None
    else:
        status = str(girl['status'])
    new = Facemash(
        first_name=str(girl['first_name']),
        last_name=str(girl['last_name']),
        status=status,
        relation=int(girl['relation']),
        vk_id=int(girl['id']),
        )
    new.photo.save("{}.jpg".format(girl['id']), djangofile)
    new.save()
    local_file.close()
    counter += 1
    print("{}/{} progress...".format(counter, sum_lens))
