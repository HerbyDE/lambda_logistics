from django.contrib.auth.decorators import user_passes_test


#Source: http://djangosnippets.org/snippets/1703
def group_required(*group_names):
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)