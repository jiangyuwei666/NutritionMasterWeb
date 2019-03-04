from mainApp.models import MyUser


def weekly_clear_user_elements():
    """
    每周一清空用户一周的营养元素摄取量
    corn表达式: 0 0 * * 1
    """
    for user in MyUser.objects.all():
        user.eaten_elements.delete()

def test():
    print('log test')