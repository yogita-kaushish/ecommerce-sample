from django.shortcuts import render,redirect,get_object_or_404
from shop.models import Products
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def products(request):
    if request.method=='GET':
        return get_products(request)
    elif request.method == 'POST':
        return create_product(request)
    else: 
        return JsonResponse({'error':'Method not Allowed'}, status=405)

@csrf_exempt
def product_detail(request,product_id):
    if request.method=='GET':
        return get_product_by_id(request,product_id)
    elif request.method == 'PUT':
        return update_product(request,product_id)
    elif request.method == 'PATCH':
        return partially_update_product(request,product_id)
    elif request.method == 'DELETE':
        return delete_product(request,product_id)
    else: 
        return JsonResponse({'error':'Method not Allowed'}, status=405)


def validate_fields(data):
    required_fields = ['name', 'description', 'price', 'stock']
    for field in required_fields:
        if field not in data:
            return False, {'error': f'Missing field: {field}'}
    return True, ''

def get_products(request):
    products = Products.objects.all()
    products_list = list(products.values())
    return JsonResponse(products_list, safe=False)

def create_product(request):
    data = json.loads(request.body)
    ret,msg = validate_fields(data)
    if not ret:
        return JsonResponse(msg, status=400)
    product = Products.objects.create(
    name=data['name'],
    description=data['description'],
    price=data['price'],
    stock=data['stock']
    )  
    return JsonResponse({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': str(product.price),
        'stock': product.stock
    }, status=201)

def update_product(request,product_id):
    try:
        product = Products.objects.get(pk=product_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    data = json.loads(request.body)
    ret, msg = validate_fields(data)
    if not ret:
        return JsonResponse(msg, status=400)
    product.name = data['name']
    product.description = data['description']
    product.price = data['price']
    product.stock = data['stock']
    product.save()
    return JsonResponse({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': str(product.price),
        'stock': product.stock
    })

def partially_update_product(request,product_id):
    try:
        product = Products.objects.get(pk=product_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    data = json.loads(request.body)
    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        try:
            product.price = float(data['price'])
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid data types for price'}, status=400)
    if 'stock' in data:
        try:
            product.stock = int(data['stock'])
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid data types for stock'}, status=400)

    product.save()
    return JsonResponse({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': str(product.price),
        'stock': product.stock
    })   
    

def delete_product(request,product_id):
    try:
        product = Products.objects.get(pk=product_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    product.delete()
    return JsonResponse({'message': 'Product deleted successfully'}, status=204)
    
def get_product_by_id(request, pk):
    try:
        product = Products.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': str(product.price),
        'stock': product.stock
    })

def list_products(request):
    response = get_products(request)
    response_bytes = response.content
    response_string = response_bytes.decode('utf-8')
    response_dict = json.loads(response_string)
    return render(request, 'ProductsList.html', {'products': response_dict})


def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        stock = request.POST.get('stock')
        price = request.POST.get('price')
        
        product = Products.objects.create(name=name, description=description, stock=stock, price=price)
        return redirect('list_products')
    return render(request, 'AddProduct.html')

def edit_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        stock = request.POST.get('stock')
        price = request.POST.get('price')
        
        product.name = name
        product.description = description
        product.stock = stock
        product.price = price
        product.save()
        
        return redirect('list_products')
    return render(request, 'EditProduct.html', {'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('list_products')
    return render(request, 'DeleteProduct.html', {'product': product})