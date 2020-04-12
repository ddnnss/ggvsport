from category.models import *

import random
def get_locals(request):
    all_cats = Category.objects.all()
    return locals()

