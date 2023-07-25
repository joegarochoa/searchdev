from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateQuerySet(request, querySet, results):
    page = request.GET.get('page')
    paginator = Paginator(querySet, results)

    try:
        querySet = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        querySet = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        querySet = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(leftIndex) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, querySet