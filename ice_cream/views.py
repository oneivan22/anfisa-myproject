from django.shortcuts import render

ice_cream_catalog = [
    {
        'id': 0,
        'title': 'Классический пломбир',
        'description': 'Настоящее мороженое, '
                       'для истинных ценителей вкуса.',
    },
    {
        'id': 1,
        'title': 'Шоколадное мороженое',
        'description': 'Нежное шоколадное мороженое. Идеально подходит для любителей насыщенного вкуса и сладкоежек.',
    },
    {
        'id': 2,
        'title': 'Мороженое со вкусом сыра чеддер',
        'description': 'Вкус сыра в вафельном стаканчике.',
    },
]


def ice_cream_list(request):
    context = {
        'ice_cream_catalog': ice_cream_catalog,
    }
    return render(request, 'ice_cream/list.html', context)


def ice_cream_detail(request, pk):
    context = {
        'ice_cream': ice_cream_catalog[pk],
    }
    return render(request, 'ice_cream/detail.html', context)