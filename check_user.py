from django.contrib.auth.models import User

try:
    u = User.objects.get(username='allan')
    print(f'Username: {u.username}')
    print(f'Is Superuser: {u.is_superuser}')
    print(f'Is Staff: {u.is_staff}')
    if hasattr(u, 'profile'):
        print(f'Role: {u.profile.role}')
    else:
        print('Role: No profile')
except User.DoesNotExist:
    print('User allan does not exist')
