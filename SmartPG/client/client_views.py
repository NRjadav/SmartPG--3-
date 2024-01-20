import random
import sys
from datetime import date

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect,HttpResponse
from .models import *

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from Admin.form import feedbackForm, wishlistForm, pgownerForm, userFrom
from Admin.models import user, area,pgtype, pgdetails, feedback, gallery, pgowner, pgfacility, facility, bookingdetails,WeekMenu,wishlist,inquiry
from datetime import date
import hashlib


def home_page(request):
    a = area.objects.all()
    p = pgdetails.objects.all()
    f = feedback.objects.all()
    t= pgtype.objects.all()
    print(a)
    print(t)
    sql1 = "SELECT pg_id_id as feedback_id , FLOOR(AVG(rate)) as AVG FROM feedback GROUP by pg_id_id"
    q = feedback.objects.raw(sql1)

    return render(request, "home_page.html",{"p": p, "f": f, "a": a, "rate": q,"t":t})


def client_header(request, id):
    p = pgdetails.objects.get(pg_id=id)
    return render(request, "client_header.html", {"p": p})


def client_login(request):
    
        try:
            if request.POST:
                email=request.POST['email']
                password=request.POST['password']
                print(email,password)
                aid=user.objects.get(email=email)
                print("ok")
                if aid.email==email :
                    if aid.password==password:
                        request.session['email']=aid.email
                        # id=request.session.get('email')
                        print("ok")
                        # print(id.id)                         
                        return  redirect("/client/home_page/")
                    else:
                        messages.success(request,"Invalid Password")
                        return render(request,"client_login.html")
                else:
                    messages.success(request,"Invalid Email")
                    return render(request,"client_login.html")
            else:
                return render(request,'client_login.html')
        except:
            messages.success(request,"Invalid Email")
            return render(request,'client_login.html')
# def client_login(request):
#     if request.method == "POST":

#         e = request.POST["email"]
#         p = request.POST["password"]
#         print("+++++++++++++++++++++",e)
        
#         uid=user.objects.get(email=e)
#         print(uid)
#     #     np = hashlib.md5(p.encode('utf')).hexdigest()
#     #     print("++++++++++++++++++++",np)

#     #     val = user.objects.filter(email=e, password=p,is_admin=0).count()

#     #     if val == 1:
#     #         val = user.objects.filter(email=e, password=np,is_admin=0)
#     #         print("+++++++++++++++++", val)
#     #         for items in val:
#     #             request.session['client_name'] = items.user_name
#     #             request.session['client_id'] = items.user_id
#         request.session['email'] = e
#         # request.session['id'] = e

#         # print(i)
#     #             print("----------",items.user_name)
#         return redirect("/client/home_page/")
#     #     else:
#     #         messages.error(request, "Invalid username and password")
#             # return render(request, "client_login.html")
#     else:
#         return render(request, "client_login.html")


# def client_forgot_password(request):
#         return render(request, "client_forgot_password.html")


def registration_show(request):
    u = user.objects.all()
    return render(request, "client_registration.html", {"user": u})


# def client_registration(request):
#     a = area.objects.all()
#     if request.method == "POST":
#         form = userFrom(request.POST)
#         print("--------", form.errors)
#         if form.is_valid():
#             try:
#                 form.save()
#                 return redirect("/client/client_login/")
#             except:
#                 print("--------", sys.exc_info())
#         else:
#             pass
#     else:
#         form = userFrom()
#         return render(request, "client_registration.html", {"form": form, "area": a})

#     return render(request, "client_registration.html", {"form": form, "area": a})
def client_registration(request):
    a = area.objects.all()
    print(a)
    if request.POST:
        name = request.POST['user_name']
        email = request.POST['email']
        password = request.POST['password']
        contact = request.POST['contact']
        area_id = request.POST['area_id']
        img=request.FILES['img']
        
        print(name, email, password, contact)


        uid = user.objects.filter(email=email).exists()

        if uid:
            print("invalid email")
            return render(request, "client_registration.html", {"area": a})
        else:
            user.objects.create(user_name=name, email=email, password=password,contact=contact, area_id_id=area_id,is_admin=0,img=img)
            request.session['email']=email
            return redirect("/client/home_page/")

    return render(request, "client_registration.html", {"area": a})

def client_forgot_password(request):
    otp1 = random.randint(10000, 99999)

    e = request.POST.get('email')
    print("---------------", e)
    request.session['client_email'] = e
    obj = user.objects.filter(email=e,is_admin=1).count()

    if obj == 1:
        data = user.objects.filter(email=e)

        request.session['client_email'] = e

        val = user.objects.filter(email=e).update(otp=otp1, otp_used=0)
        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject, message, email_from, recipient_list)
        return render(request, "reset_password.html")

    else:
        messages.error(request, "Invalid User Name or Password")
        return render(request, "client_forgot_password.html")


def set_password(request):
    totp = request.POST['otp']
    print("+++++++++++otp_++++++++++++++++++++", totp)
    tpassword = request.POST.get('npass')
    cpassword = request.POST.get('cpass')

    if tpassword == cpassword:
        e = request.session['client_email']
        val = user.objects.filter(email=e, is_admin=0, otp=totp, otp_used=0).count()

        if val == 1:
            print("ok1")
            # tp = hashlib.md5(tpassword.encode('utf')).hexdigest()
            val = user.objects.filter(email=e, is_admin=0).update(otp_used=1, password=tpassword)
            return redirect('/client/client_login/')
        else:
            print("ok2")

            messages.error(request, 'OTP does not match')
            return render(request, "reset_password.html")
    else:
        print("ok3")

        messages.error(request, 'New Password & Confirm Password does not match')
        return render(request, "reset_password.html")

    return render(request, "reset_password.html")


def hostel_view(request):
    a = area.objects.all()
    p = pgdetails.objects.all()
    t= pgtype.objects.all()
    sql1 = "SELECT pg_id_id as feedback_id , FLOOR(AVG(rate)) as AVG FROM feedback GROUP by pg_id_id"
    q = feedback.objects.raw(sql1)
    # rows='''SELECT pg_id_id as ID , AVG(rate) as AVG FROM feedback GROUP by pg_id_id'''
    # print(rows)
    # qs=feedback.objects.raw(rows)

    print("++++++++++++++++++++++",q)

    page = request.GET.get('page', 1)
    print("page ----------------", page)
    paginator = Paginator(p, 6)

    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)
    return render(request, "hostel-grid-view.html", {"a": a,"t": t, "pd": qs,"rate":q})


def list_view(request):
    u = request.session['email']
    print(u)
    c = user.objects.get(email=u)
    a = area.objects.all()
    p = pgdetails.objects.all()
    sql1 = "SELECT pg_id_id as feedback_id , FLOOR(AVG(rate)) as AVG FROM feedback GROUP by pg_id_id"
    q = feedback.objects.raw(sql1)
    print("----", q)
    page = request.GET.get('page', 1)
    print("page ----------------", page)
    paginator = Paginator(p, 3)

    try:
        qs1 = paginator.page(page)
    except PageNotAnInteger:
        qs1 = paginator.page(1)
    except EmptyPage:
        qs1 = paginator.page(paginator.num_pages)

    return render(request, "hostel-list-view.html", {"a":a,"qs1":qs1, "rate":q, "p":p,"c":c})


def hostel_page(request,id=0):
    pf = pgfacility.objects.filter(pg_facility_id=id)
    f1 = pgfacility.objects.filter(pg_id_id=id)
    a = area.objects.filter(area_id=id)
    po = pgowner.objects.filter(owner_id=id)

    u = user.objects.filter(user_id=id)
    p = pgdetails.objects.filter(pg_id=id)
    p1=pgdetails.objects.get(pg_id=id)
    print(p1.pg_id)
    f = feedback.objects.filter(pg_id_id=id)
    g = gallery.objects.filter(pg_id_id=id)
    week_menu = WeekMenu.objects.filter(pg_id_id=id)
    return render(request, "hostel-single-page.html", {"f": f, "g":g, "p":p, "u":u, "id":id ,"po":po, "a":a, "pf":pf, "f1": f1,"p1":p1.pg_id,'week_menu': week_menu})


def client_edit(request):
    u = request.session['email']
    print(u)
    c = user.objects.get(email=u)
    a = area.objects.all()
    print("++++++++++++++++++++++++++++++++++++++++++++", c)
    return render(request,"user_edit_profile.html", {"u": c, "area": a})


def client_update(request):
    u = request.session['email']
    c = user.objects.get(email=u)
    a = area.objects.all()

    if request.POST:
        user_name=request.POST['user_name']
        email=request.POST['email']
        password=request.POST['password']
        contact=request.POST['contact']
        a1=request.POST['area_id']
        
        print(user_name,email,password,contact)
        c.user_name=user_name
        c.email=email
        c.password=password
        c.contact=contact
        a2=area.objects.get(area_id=a1)
        c.area_id=a2
        c.save()
    # a = area.objects.all()
    # print("++++++++++++++++++++++++++++++++",c)
    # if request.method == "POST":
    #     form = userFrom(request.POST, instance=c)
    #     print("---ok-----", form.errors)
    #     if form.is_valid():
    #         try:
    #             form.save()
    #             return redirect("/client/home_page/")
    #         except:
    #             print("--------", sys.exc_info())
    #     else:
    #         return render(request, "user_edit_profile.html", {"form":form,"u": c, "area": a})

    return render(request, "user_edit_profile.html", {"u": c,"area": a})


def client_logout(request):
    try:
        del request.session['client_id']
        del request.session['client_name']
        del request.session['client_email']

    except:
        pass

    return redirect("/client/client_login/")


def owner_logout(request):
    try:
        del request.session['owner_id']
        del request.session['owner_name']
        del request.session['email']

    except:
        pass

    return redirect("/client/owner_login/")


def load_menu(request):
    a = area.objects.all()
    return render(request, "test.html", {"a":a})


def user_dashboard(request, id = 0):
    if "email" in request.session:
        p = pgdetails.objects.filter(pg_id=id)
        i = request.session['email']
        print("-------------",i)
        u = user.objects.filter(email=i)
        return render(request, "user-dashboard.html", {"u": u, "p": p})
    else:
        print("ok")
        return render(request, "user-dashboard.html")


# def user_booking(request, id = 0):
#     id = request.session['email']
#     uid=user.objects.get(email=id)
#     print(uid.user_id)
#     b = bookingdetails.objects.filter(user_id =uid.user_id)
#     return render(request, "user-dashboard-booking.html", {"b": b})

import razorpay
def user_booking(request, id=0):
   
        # Handling Razorpay payment initiation
        # Convert the price to paisa
    id = request.session['email']
    uid = user.objects.get(email=id)
    b = bookingdetails.objects.filter(user_id=uid.user_id)
    l1=[]
    for v in b:
        l1.append(v.pg_id.amount)
    amount=sum(l1)*100
    print(amount)
    client = razorpay.Client(auth=('rzp_test_bilBagOBVTi4lE','77yKq3N9Wul97JVQcjtIVB5z'))

    if amount>=100:
        payment_order = client.order.create({
            'amount': 100,
            'currency': 'INR',
            'payment_capture': '1'  # Auto capture the payment when successfully done
        })

        order_id = payment_order['id']
        order_amount = payment_order['amount']
        print("hjdashfa",order_amount)

        return render(request, 'user-dashboard-booking.html', {'order_id': order_id, 'order_amount': 1000,"b": b})
    else:
        return render(request, 'user-dashboard-booking.html', {"b": b})

        # Handling Razorpay payment success callback
        

# def feedback_insert(request):

#     if request.POST:
#         try:
#             id = request.session['email']
#             uid=user.objects.get(email=id)
#             d = date.today()
#             u1=2
            
#             desc=request.POST['feedback']
#             rate=request.POST["rate"]
#             print(uid,d,desc,rate,u1) 
#             feedback.objects.create(date=d,rate=rate,user_id=uid,pg_id=u1,des=desc)
#             # form=feedback(des=desc,user_id=uid,pg_id_=u1,date=d,rate=rate)
#             print("ok1")
#             # form.save()
#             return redirect("/client/hostel_page/%s" % id)

#         except:
#             print("++++++++++++++",sys.exc_info())
#     # return redirect("/client/hostel_page/%s" % id)
#     print("ok")
#     feedback.objects.create(date=d,rate=rate,user_id=uid,pg_id=u1,des=desc)
#     return render(request,"hostel-single-page.html")


# def feedback_insert(request):
#     if request.POST:

#         id = request.session['email']
#         uid=user.objects.get(email=id)
#         pg_id=request.POST["pg_id"]
#         print(pg_id)
       

#         d = date.today()
#         u1=2
#         desc=request.POST['feedback']
#         rate=request.POST["rate"]
#         print(uid,d,desc,rate,pg_id) 
#         f = feedback.objects.filter(pg_id_id=pg_id)
#         feedback.objects.create(date=d,rate=rate,user_id=uid,pg_id_id=pg_id,des=desc)
#     return render(request,"hostel-single-page.html",{"f":f})

def feedback_insert(request):
    try:
        if request.POST:
            id = request.session.get('email')  # Using get to avoid KeyError if 'email' is not in the session
            uid = user.objects.get(email=id)
            pg_id = request.POST.get("pg_id")  # Using get to avoid KeyError if 'pg_id' is not in the request.POST
            print(pg_id)

            d = date.today()
            desc = request.POST.get('feedback', '')
            rate = request.POST.get("rate", '')

            if rate:  # Check if 'rate' is not empty
                print(uid, d, desc, rate, pg_id)
                
                # Assuming you want to filter by user and pg_id, not sure what u1 is for
                f = feedback.objects.filter(user_id=uid, pg_id_id=pg_id)
                
                feedback.objects.create(date=d, rate=rate, user_id=uid, pg_id_id=pg_id, des=desc)
                return redirect("/client/hostel_page/%s" % pg_id)
            else:
                # Handle the case where 'rate' is empty
                feedback.objects.create(date=d,rate=0 ,user_id=uid, pg_id_id=pg_id, des=desc)

                return redirect("/client/hostel_page/%s" % pg_id)
                
        
        return render(request, "hostel-single-page.html",{"pg_id":pg_id})
    except:
        return render(request, "hostel-single-page.html")


    
def booking_insert(request):
    # bid=bookingdetails.objects.a
    if request.POST:
            id = request.session['email']
            uid=user.objects.get(email=id)
            bd = date.today().strftime("%Y-%m-%d")
            print("dsdsaf",uid)
            pid = request.POST["pg_id"]
            status=request.POST["booking_status"]
            print(bd,uid,pid,status)
            form = bookingdetails(user_id=uid,pg_id_id=pid,booking_date=bd,booking_status=status)
            form.save()
            # return redirect("/client/hostel_view/")
            return redirect("/client/user_booking/")
    # return redirect("/client/hostel_view/%s" % pid)
    return render(request, "hostel-grid-view.html")


def display_pg(request):
    pg=request.POST.get("selectpg")
    a=request.POST.get("selectbasic")
    t= pgtype.objects.all()
    print("------",pg,"----------",a,pg)
    p = pgdetails.objects.filter(area_id_id=a,pgtype_id=pg)
    a = area.objects.all()
    print("========",p)

    return render(request,"hostel-grid-view.html",{"pd":p,"a":a,"t":t})


def wishlist_show(request):
    wish = wishlist.objects.all()
    p = pgdetails.objects.all()
    sql1 = "SELECT pg_id_id as feedback_id , FLOOR(AVG(rate)) as AVG FROM feedback GROUP by pg_id_id"
    q = feedback.objects.raw(sql1)

    return render(request, "user-dashboard-wishlist.html",{"wish":wish,"p":p, "rate":q})


def insert_wishlist(request):

    if request.method == "POST":
        try:
            d = date.today().strftime("%Y-%m-%d")
            p_id = request.POST["pg_id"]
            print(d,p_id)
            u = request.session['email']
            uid= user.objects.get(email=u)
            print(d,p_id,uid.user_id)
            pid=pgdetails.objects.get(pg_id=p_id)

            wishlist.objects.create(date=d, pg_id_id=p_id, user_id=uid,img=pid.img)
            return redirect("/client/wishlist/")
        except:
            print("----------", sys.exc_info())
    else:
        return render(request, "user-dashboard-wishlist.html")
    return render(request, "user-dashboard-wishlist.html")


def wish_delete(request,id):
    wish = wishlist.objects.get(wishlist_id=id)
    wish.delete()
    return redirect("/client/wishlist/")


def area_pg(request,id):
    p=pgdetails.objects.filter(area_id=id)
    return render(request, "hostel-grid-view.html", {"pd": p})


def client_inquiry(request):
    u = user.objects.all()
    print(u)    
    return render(request, "contact-us-page.html", {"u":u})


def insert_inquiry(request):
    if request.method == "POST":
        try:
            u = request.session['email']
            uid1= user.objects.get(email=u)
            uid = uid1.user_id
            email = uid1.email
            type = request.POST.get("inquiry_type")
            title = request.POST.get("inquiry_title")
            contact = request.POST['contact']
            print(uid,email,type,title,contact)
            form = inquiry(user_id_id=uid,inquiry_type=type,inquiry_title=title, email=email,contact=contact)
            form.save()
            return redirect("/client/client_inquiry/")
        except:
            print("----------",sys.exc_info())

    return redirect("/client/client_inquiry/")


def partner_dashboard(request):
    return render(request, "partner-dashboard.html")


def order_dashboard(request):
    return render(request, "partner-my-order-dashboard.html")


def manage_dashboard(request):
    return render(request, "partner-manage-service-dashboard.html")


def inbox_dashboard(request):
    return render(request, "partner-inbox-dashboard.html")


def withdraw(request):
    return render(request, "partner-withdraw-dashboard.html")


def sort_data(request):
    id = request.GET.get('sort')
    print("---- SORT 000000000000",id)
    sql1 = "SELECT pg_id_id as feedback_id , FLOOR(AVG(rate)) as AVG FROM feedback GROUP by pg_id_id"
    q = feedback.objects.raw(sql1)
    if id == '1':
        p = pgdetails.objects.all().order_by("amount")
    elif id == '3':
        p = pgdetails.objects.all().order_by("pg_name")
        print(p)   
    elif id == '4':
        p = pgdetails.objects.all().order_by("-pg_name")
        print(p)       
    else:
        p = pgdetails.objects.all().order_by("-amount")

    return render(request,"sort.html",{"product":p, "rate":q})


def data_sort(request):
    id = request.GET.get('sort')
    print("---- SORT 11111",id)
    sql1 = "SELECT pg_id_id as feedback_id , FLOOR(AVG(rate)) as AVG FROM feedback GROUP by pg_id_id"
    q = feedback.objects.raw(sql1)
    print("bjkdashfk",id)
    if id == '1':
        p = pgdetails.objects.all().order_by("pg_name")
        print(p)
    else:
        p = pgdetails.objects.all().order_by("-pg_name")
        print(p)  
    return render(request, "short.html", {"product":p, "rate":q})


def price_filter(request):
    s = request.GET.get('start')
    e = request.GET.get('end')
    print("--- Price Filter---")
    id = request.GET.get('sort')
    print("---- SORT 000000000000",id)
    sql1 = "SELECT pg_id_id as feedback_id , FLOOR(AVG(rate)) as AVG FROM feedback GROUP by pg_id_id"
    q = feedback.objects.raw(sql1)

    p = pgdetails.objects.filter(amount__range=[int(s), int(e)])

    for data in p:
        print("+++", data.amount)
    return render(request, "list_short.html", {"product":p, "rate":q})

def payment_success(request):
    if request.method == 'POST':
        # Handle payment success logic here
        return render(request, 'payment/success.html')

    return render(request, 'payment/error.html')