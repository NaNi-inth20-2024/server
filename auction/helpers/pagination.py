def create_paginated_dict(paginator, page_obj, objects, limit, base_url):
    next_url = None if not page_obj.has_next() else f'{base_url}?limit={limit}&offset={page_obj.next_page_number() * limit}'
    prev_url = None if not page_obj.has_previous() else f'{base_url}?limit={limit}&offset={page_obj.previous_page_number() * limit}'
    return {
        'count': paginator.count,
        'next': next_url,
        'previous': prev_url,
        'results': objects,
    }
