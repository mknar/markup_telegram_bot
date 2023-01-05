from markup_tool.models import Object, Classification


def statistics_of_marked_data(request):
    extra_context = {}
    if request.path == '/admin/':
        extra_context['all_objects_count'] = Object.objects.count()
        extra_context['marked_objects_count'] = Object.objects.filter(marked=True).count()
        extra_context['classifications'] = Classification.objects.filter(marking_tasks__isnull=False).distinct().prefetch_related(
            'marking_tasks')
    return extra_context
