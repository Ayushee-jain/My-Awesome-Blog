from django.shortcuts import render
from django.http import HttpResponse
from .models import Contact, Product, Orders, OrderUpdate
from math import ceil
import json
# Create your views here.


def index(request):
    # products=Product.objects.all()
    # n=len(products)
    # nSlides=n//4+ceil((n/4)-(n//4))
    allProds=[]
    catprods=Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n=len(prod)
        nSlides=n//4+ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nSlides),nSlides])


    # params={'no_of_silde': nSlides,'range':range(1,nSlides),'product':products}
    # for heading of product list of list
    # allProds=[[products,range(1,nSlides),nSlides],[products,range(1,nSlides),nSlides]]
    params={'allProds':allProds}
    return render(request,'shop/index.html',params)

def searchMatch(query,item):
    # print(item)
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.subcategory.lower():
        return True
    else:
        return False

def search(request):
    query=request.GET.get('search')
    allProds=[]
    catprods=Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prodtemp=Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n=len(prod)
        nSlides=n//4+ceil((n/4)-(n//4))
        if len(prod)!=0:
            allProds.append([prod,range(1,nSlides),nSlides])
    params={'allProds':allProds,'msg':""}
    if len(allProds)==0:
        params={'msg':"Plase make sure to enter relevent search query"}
    return render(request,'shop/search.html',params)

def about(request):
    return render(request,'shop/about.html') 

def contact(request):
    if request.method=="POST":
        # print(request)
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        # print(name,email,phone,desc)
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thanks=True
        return render(request,'shop/contact.html',{'thanks':thanks})
    return render(request,'shop/contact.html')

def tracker(request):
    if request.method=="POST":
        orderId=request.POST.get('orderId','')
        email=request.POST.get('email','')
        try:
            order=Orders.objects.filter(order_id=orderId,email=email)
            if len(order)>0:
                update=OrderUpdate.objects.filter(order_id=orderId)
                updates=[]
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response=json.dumps({"status":"success","updates":updates,"itemsJson":order[0].items_json},default=str) #The json.dumps() is used when we want to convert dictionary to json format 
                return HttpResponse(response)
            else:
                return HttpResponse({"status":"noitem"})
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request,'shop/tracker.html')


def productView(request,myid):
    # fetch the product using id
    product=Product.objects.filter(id=myid)
    # print(product)
    return render(request,'shop/prodview.html',{'product':product[0]})

def checkout(request):
    if request.method=="POST":
        # print(request)
        items_json=request.POST.get('itemsJson','')
        name=request.POST.get('name','')
        amount=request.POST.get('amount','')
        email=request.POST.get('email','')
        address=request.POST.get('address1','')+request.POST.get('address2','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip_code=request.POST.get('zip_code','')
        phone=request.POST.get('phone','')
        # print(name,email,phone,desc)
        order=Orders(items_json=items_json,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone, amount=amount)
        order.save()
        update=OrderUpdate(order_id=order.order_id,update_desc="The order has been placed")
        update.save()
        thank=True
        id=order.order_id
        return render(request,'shop/checkout.html',{'thank':thank,'id':id})
    return render(request,'shop/checkout.html')

