from .utils import JsonResponse, api_method
from .forms import FirstTaskForm


@api_method('GET', FirstTaskForm)
def first_task(request, form):
    print(form['number'])
    return JsonResponse.success({'ok': form['number']})
