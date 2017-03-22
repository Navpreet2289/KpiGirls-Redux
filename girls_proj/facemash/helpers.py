from django.core.cache import cache


def get_client_ip(request):
    '''
    Getting ip adress here
    '''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def cache_hits(id, request):
    '''
    Checking cache for available key(post id) and value(set() with ip adresses)
    and if None creating it and adding ip address to it
    '''
    key = 'girl_{}'.format(id)
    client_ip = get_client_ip(request)
    result = cache.get(key, [set(), 0])
    if client_ip not in result[0]:
        result[0].add(client_ip)
        result[1] += 1
        cache.set(key, result, None)


def get_top_girls():
    '''
    Getting top 100 girls by hits number
    '''
    cached = cache.get("cached_result")
    if cached:
        return cached

    name_list = [post for post in cache.iter_keys("girl_*")]
    result_post_dict = cache.get_many(name_list)
    sorted_post_list = sorted(result_post_dict.items(), key=lambda e: e[1][1], reverse=True)
    top_ids_list = [int(top_post[0].split('_')[1]) for top_post in sorted_post_list[:100]]
    cache.set("cached_result", top_ids_list, timeout=90)
    return top_ids_list
