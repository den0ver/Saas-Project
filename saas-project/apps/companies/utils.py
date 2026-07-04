from .models import Company


def get_user_company(user):
    return Company.objects.filter(owner=user).first()