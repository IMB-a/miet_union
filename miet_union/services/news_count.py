def news_count(all_news, context):
    news_count = 0
    for news in all_news:
        news_count += 1
    context.update({'news_count': news_count})
    return context
