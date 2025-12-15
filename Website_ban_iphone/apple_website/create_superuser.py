from django.contrib.auth import get_user_model

username = 'admin'
email = 'admin@example.com'
password = 'AdminPass123'

User = get_user_model()

if User.objects.filter(username=username).exists():
    print(f"Superuser '{username}' already exists.")
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Created superuser '{username}' with password '{password}'.")
