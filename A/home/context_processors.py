from .models import Product


def product_slug(request):
    if request.session['cart']:
        session = request.session['cart'].keys()
        result_id = int(list(session)[0])
        product = Product.objects.get(id=result_id)
        return {
            'product': product
        }
    return {}
