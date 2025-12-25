from .models import Purchase

def cart_count(request):
    if request.user.is_authenticated:
        return {'cart_count': Purchase.objects.filter(user=request.user).count()}
    return {'cart_count': 0}
