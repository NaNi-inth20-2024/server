def create_paginated_dict(paginator, page_obj, objects, limit, base_url):
    """
    Converts paginated data into a dictionary suitable for JSON serialization.

    :param paginator: The Paginator object used for pagination.
    :param page_obj: The Page object representing the current page.
    :param objects: The paginated objects to include in the results.
    :param limit: The limit of objects per page.
    :param base_url: The base URL used for constructing next and previous page URLs.
    :return: A dictionary representing the paginated data.
    """

    next_url = None if not page_obj.has_next() else f'{base_url}?limit={limit}&offset={page_obj.next_page_number() * limit}'
    prev_url = None if not page_obj.has_previous() else f'{base_url}?limit={limit}&offset={page_obj.previous_page_number() * limit}'
    return {
        'count': paginator.count,
        'next': next_url,
        'previous': prev_url,
        'results': objects,
    }
