from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def make_paginator(request, all_news, context):
    """
    123
    """
    paginator = Paginator(all_news, 5)

    page = request.GET.get('page')
    try:
        all_news = paginator.page(page)
    except PageNotAnInteger:
        all_news = paginator.page(1)
    except EmptyPage:
        all_news = paginator.page(paginator.num_pages)
    context.update({'all_news': all_news})
    return context
