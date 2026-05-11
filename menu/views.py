from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, MenuItem, Customer, Order, OrderItem


def menu_list(request):
    """Главная страница – меню, сгруппированное по категориям"""
    categories = Category.objects.prefetch_related('menuitem_set').all()
    return render(request, 'menu/menu_list.html', {'categories': categories})


def create_order(request):
    """Обработка формы заказа"""
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email', '')
        comment = request.POST.get('comment', '')
        
        # Создаём или находим клиента по телефону
        customer, created = Customer.objects.get_or_create(
            phone=phone,
            defaults={'name': name, 'email': email}
        )
        
        # Создаём заказ
        order = Order.objects.create(
            customer=customer,
            comment=comment
        )
        
        # Обрабатываем выбранные блюда
        # Поля с количеством называются 'item_<id>'
        for key, value in request.POST.items():
            if key.startswith('item_') and value.isdigit():
                quantity = int(value)
                if quantity > 0:
                    item_id = int(key.split('_')[1])
                    menu_item = MenuItem.objects.get(id=item_id)
                    OrderItem.objects.create(
                        order=order,
                        menu_item=menu_item,
                        quantity=quantity
                    )
        
        # Если ни одного блюда не выбрано – возвращаем форму с ошибкой
        if not order.items.exists():
            order.delete()
            # Если клиент был только что создан и заказ пустой – удалим и клиента
            if created:
                customer.delete()
            menu_items = MenuItem.objects.select_related('category').all()
            return render(request, 'menu/create_order.html', {
                'menu_items': menu_items,
                'error': 'Добавьте хотя бы одно блюдо в заказ'
            })
        
        return redirect('order_success', order_id=order.id)
    
    # GET-запрос – показываем форму
    menu_items = MenuItem.objects.select_related('category').all()
    return render(request, 'menu/create_order.html', {'menu_items': menu_items})


def order_success(request, order_id):
    """Страница успешного оформления заказа"""
    order = get_object_or_404(Order, id=order_id)
    total = sum(item.total_price for item in order.items.all())
    return render(request, 'menu/order_success.html', {
        'order': order,
        'total': total
    })