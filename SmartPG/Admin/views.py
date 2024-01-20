import hashlib

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from Admin.models import user
from Admin.models import area
from Admin.models import pgdetails
from Admin.models import bookingdetails
from Admin.models import facility
from Admin.models import feedback
from Admin.models import gallery
from Admin.models import inquiry
from Admin.models import pgowner
from Admin.models import pgfacility
from django.contrib import messages
from django.core.mail import send_mail
from Admin.form import pgdetailsForm, areaForm, facilityForm, galleryForm, inquiryForm, feedbackForm,userFrom
import random
from smartpg import settings
import sys
from Admin.function import handle_uploaded_file
from django.db import connection
from django.shortcuts import render
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date

# Create your views here.


def delete(request, id):
    a = area.objects.get(area_id=id)
    a.delete()
    return redirect("/area/")


def facility_delete(request, facility_id):
    f = facility.objects.get(facility_id=facility_id)
    f.delete()
    return redirect("/facility_show/")


def pgdetails_delete(request, pg_id):
    pd = pgdetails.objects.get(pg_id=pg_id)
    pd.delete()
    return redirect("/owner_pgowner/")


def gallery_delete(request, gallery_id):
    g = gallery.objects.get(gallery_id=gallery_id)
    g.delete()
    return redirect("/gallery_show/")


def feedback_delete(request, feedback_id):
    f = feedback.objects.get(feedback_id=feedback_id)
    f.delete()
    return redirect("/feedback_show/")


def inquiry_delete(request, inquiry_id):
    i = inquiry.objects.get(inquiry_id=inquiry_id)
    i.delete()
    return redirect("/inquiry/")


def bookingdetails_show(request):
    b = bookingdetails.objects.all()
    p = pgdetails.objects.all()
    return render(request, "bookingdetails.html", {"b": b,"p":p})


def update_b(request):
    p = pgdetails.objects.all()
    return render(request, "bookingdetails.html", {"p":p,"pg_id":1})


def facility_show(request):
    f = facility.objects.all()
    return render(request, "facility.html", {'facility': f})


def feedback_show(request):
    f = feedback.objects.all()

    return render(request, "feedback.html", {"fb": f})


def feedback_insert(request):
    u = user.objects.all()
    pd = pgdetails.objects.all()
    if request.method == "POST":
        form = feedbackForm(request.POST)
        print("-------", form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect("/feedback_show")
            except:
                print("-------", sys.exc_info())
        else:
            pass
    else:
        form = feedbackForm()
        return render(request, "feedback_insert.html", {"form": form , "u":u, "pd":pd})

    return render(request, "feedback_insert.html", {"form": form , "u":u, "pd":pd})


def feedback_edit(request, feedback_id):
    f = feedback.objects.get(feedback_id=feedback_id)
    return render(request, "feedback_edit.html", {"feedback": f})


def feedback_update(request, feedback_id):
    f = feedback.objects.get(feedback_id=feedback_id)
    form = feedbackForm(request.POST, instance=f)

    print("-----", form.errors)
    if form.is_valid():
        try:
            form.save()
            return redirect("/feedback")
        except:
            print("-----", sys.exc_info())

        return render(request, "feedback_edit.html", {"feedback": f})


def gallery_show(request):
    g=gallery.objects.all()
    return render(request, "gallery.html",{'g':g})


def pgowner_show(request):
    o = pgowner.objects.all()
    return render(request, "pgowner.html", {'pgowner': o})


def pgfacility_show(request, id=5):
    p = pgfacility.objects.all()
    print(p)
    return render(request, "pgfacility.html", {"pf": p})


def view(request):
    u = user.objects.all()
    return render(request, "user.html", {"user": u})


def admin_login(request):

    if request.method == "POST":

        e = request.POST.get("email")
        p = request.POST.get("pass")

        val = user.objects.filter(email=e,password=p,is_admin=1).count()

        if val == 1:
            data = user.objects.filter(email=e,password=p)
            print("++++++++", data)
            for items in data:
                request.session['username'] = items.user_name
                request.session['id'] = items.user_id
                request.session['email'] = items.email
                return redirect('/view/')

        else:
            messages.error(request, "Invalid username and password")
            return render(request, "login.html")
    else:
            return render(request, "login.html")


def forgot_password(request):
    return render(request, "forgot_password.html")


def Send_OTP(request):
    otp1 = random.randint(10000, 99999)

    e = request.POST.get('email')
    print("---------------", e)
    request.session['email'] = e
    obj = user.objects.filter(email=e,is_admin=1).count()

    if obj == 1:
        data = user.objects.filter(email=e,is_admin=1)

        request.session['admin_email'] = e

        val = user.objects.filter(email=e).update(otp=otp1, otp_used=0)
        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject, message, email_from, recipient_list)
        return render(request, "reset.html")

    else:
        messages.error(request, "Invalid User Name or Password")
        return render(request, "forgot_password.html")


def set_password(request):
    totp = request.POST['otp']
    print("+++++++++++otp_++++++++++++++++++++",totp)
    tpassword = request.POST.get('npass')
    cpassword = request.POST.get('cpass')

    if tpassword == cpassword:
        e = request.session['email']
        val = user.objects.filter(email=e, is_admin=1, otp=totp, otp_used=0).count()

        if val == 1:
            val = user.objects.filter(email=e, is_admin=1).update(otp_used=1, password=tpassword)
            return redirect('/login/')
        else:
            messages.error(request, 'OTP does not match')
            return render(request, "reset.html")
    else:
        messages.error(request, 'New Password & Confirm Password does not match')
        return render(request, "reset.html")

    return render(request, "reset.html")


def area_show(request):
    a = area.objects.all()
    return render(request, "area.html", {"area": a})


def area_insert(request):
    if request.method == "POST":
        form = areaForm(request.POST)
        print("-------", form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect("/area")
            except:
                print("-------", sys.exc_info())
        else:
            pass
    else:
        form = areaForm()
        return render(request, "area_insert.html", {"form": form})

    return render(request, "area_insert.html", {"form": form})


def pgdetails_show(request):
    pd = pgdetails.objects.all()
    a = area.objects.all()
    return render(request, "pgdetails.html", {"pd": pd, "a": a})


def pgdetails_insert(request):
    po = pgowner.objects.all()
    a = area.objects.all()
    if request.method == "POST":
        form = pgdetailsForm(request.POST,request.FILES)
        print("-------", form.errors)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['img'])
                form.save()
                return redirect("/pgdetails")
            except:
                print("-------", sys.exc_info())
        else:
            pass
    else:
        form = pgdetailsForm()
        return render(request, "pgdetails_insert.html", {"form": form,"a":a, "po":po})

    return render(request, "pgdetails_insert.html", {"form": form,"a":a, "po":po})


def pgdetails_edit(request, pg_id):
    p = pgdetails.objects.get(pg_id=pg_id)
    return render(request, "pgdetails_edit.html", {"pd": p})


def pgdetails_update(request, pg_id):
    p = pgdetails.objects.get(pg_id=pg_id)

    print("+++++++++++",p)
    if request.method == "POST":
        form = pgdetailsForm(request.POST, instance=p)
        print("--------", form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect("/pgdetails_show")
            except:
                print("--------", sys.exc_info())
        else:
            return render(request, "pgdetails_edit.html", {"form":form, "pd": p})

    return render(request, "pgdetails_edit.html", {"pd": p})
    
    
def admin_edit(request):
    u = request.session['id']
    c = user.objects.get(user_id=u,is_admin=1)
    a = area.objects.all()
    print("++++++++++++++", c)
    return render(request, "admin_edit.html", {"u": c, "area": a})


def admin_update(request):
    u = request.session['id']
    c = user.objects.get(user_id=u)
    a = area.objects.all()
    print("+++++++++++",c)
    if request.method == "POST":
        form = userFrom(request.POST, instance=c)
        print("--------", form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect("/view/")
            except:
                print("--------", sys.exc_info())
        else:
            return render(request, "admin_edit.html", {"form":form, "u": c, "area": a})

    return render(request, "admin_edit.html", {"u": c,"area":a})


def facility_insert(request):
    if request.method == "POST":
        form = facilityForm(request.POST)
        print("-------", form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect("/facility/")
            except:
                print("-------", sys.exc_info())
        else:
            pass
    else:
        form = facilityForm()
        return render(request, "facility_insert.html", {"form": form})

    return render(request, "facility_insert.html", {"form": form})


def gallery_insert(request):
    p = pgdetails.objects.all()
    if request.method == "POST":
        form = galleryForm(request.POST, request.FILES)
        print("-------", form.errors)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['gallery_name'])
                form.save()
                return redirect('/gallery_show/')
            except:
                print("--------",sys.exc_info())
        else:
            pass
    else:
        form = galleryForm()
        return render(request, "gallery_insert.html",{'form': form, "p": p})

    return render(request, "gallery_insert.html")


def inquiry_show(request):
    i = inquiry.objects.all()
    return render(request, "inquiry.html", {"inquiry": i})


def edit(request, area_id):
    a = area.objects.get(area_id=area_id)
    return render(request, "edit.html", {"area": a})


def update(request, id):
    a = area.objects.get(area_id=id)
    form = areaForm(request.POST, instance=a)

    print("-----", form.errors)
    if form.is_valid():
        try:
            form.save()
            return redirect("/area/")
        except:
            print("-----", sys.exc_info())

        return render(request, "edit.html", {"area": a})


def facility_edit(request, facility_id):
    f = facility.objects.get(facility_id=facility_id)
    return render(request, "facility_edit.html", {"facility": f})


def facility_update(request, facility_id):
    f = facility.objects.get(facility_id=facility_id)
    form = facilityForm(request.POST, instance=f)

    print("-----", form.errors)
    if form.is_valid():
        try:
            form.save()
            return redirect("/facility")
        except:
            print("-----", sys.exc_info())

        return render(request, "facility_edit.html", {"facility": f})


class projectChart(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self,request,format=None):
        cursor=connection.cursor()
        cursor.execute(''' SELECT (SELECT pg_name from pgdetails where pg_id = b.pg_id_id) as "PG" , count(*) "TOTAL" FROM bookingdetails b JOIN pgdetails p where b.pg_id_id = p.pg_id GROUP by b.pg_id_id''')
        qs=cursor.fetchall()
        print("+++++++++++=")
        labels=[]
        default_items=[]
        for item in qs:
            labels.append(item[0])
            default_items.append(item[1])

        data = {
            "labels": labels,
            "default": default_items,
        }
        return Response(data)


def index(request):
    u = user.objects.all().count()
    b = bookingdetails.objects.all().count()
    p = pgdetails.objects.all().count()
    d = date.today()
    f = feedback.objects.all()
    bd = bookingdetails.objects.filter(booking_status=0)
    return render(request, "index.html", {"user": u, "b": b, "p":p, "f":f ,"bd":bd})


class HomeView(View):
    u = user.objects.all()
    def get(self,request,*args,**kwargs):
        return render(request,"index.html")


def accept(request, booking_id):
    b = bookingdetails.objects.get(booking_id=booking_id)
    b.booking_status = 1
    b.save()
    return redirect('/bookingdetails_show/','/index/')


def reject(request, booking_id):
    b = bookingdetails.objects.get(booking_id=booking_id)
    b.booking_status = 2
    b.save()
    return redirect('/bookingdetails_show/')


def header(request):
    bd = bookingdetails.objects.all()
    return render(request, "header.html", {"bd":bd})


def logout(request):

    try:
        del request.session['user_id']
        del request.session['user_name']
        del request.session['email']

    except:
        pass

    return redirect("/login/")

@csrf_exempt
def bookingdetails1(request):

    if request.method == "POST":
        start = request.POST["sd"]
        end = request.POST["ed"]

        start = parse_date(start)
        end = parse_date(end)
        if start < end:

             b=bookingdetails.objects.filter(booking_date__range=[start, end])
             return render(request, "bookingdetails1.html", {"b":b})
        else:
            b =  bookingdetails.objects.all()
            msg = messages.error(request,"start date must be smaller tha end date")
            return render(request, "bookingdetails1.html", {"b":b, "message":msg})
    else:
        b =  bookingdetails.objects.all()

        return render(request, "bookingdetails1.html", {"b":b})


@csrf_exempt
def bookingdetails2(request):

    p = pgdetails.objects.all()
    b = bookingdetails.objects.all()
    if request.method == "POST":
        id = request.POST.get('pgid')
        print("-----------", id)
        b = bookingdetails.objects.filter(pg_id_id=id)
        return render(request, "data.html", {"b": b})
    else:
        return render(request, "bookingdetails2.html", {"b":b, "p":p})


def data(request):
    b = bookingdetails.objects.all()
    return render(request, "data.html", {"b": b})


def customer_count_report(request):

    sql1 = " SELECT (select user_name from user where user_id = b.user_id_id) as name,  count(*) as booking_id FROM bookingdetails b JOIN user u where b.user_id_id = u.user_id GROUP by user_id_id "

    data = bookingdetails.objects.raw(sql1)

    return render(request, "countreport.html", {"data": data})


def pgfacility_insert(request):
    a = area.objects.all()
    if request.method == "POST":
        form = pgdetailsForm(request.POST,request.FILES )
        print("-------", form.errors)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['img'])
                form.save()
                return redirect("/pgfacility")
            except:
                print("-------", sys.exc_info())
        else:
            pass
    else:
        form = pgdetailsForm()
        return render(request, "pgfacility_insert.html", {"form": form,"a":a})

    return render(request, "pgfacility_insert.html", {"form": form,"a":a})


def pgfacility_edit(request, pg_id):
    pd = pgdetails.objects.get(pg_id=pg_id)
    return render(request, "pgfacility_edit.html", {"pd": pd})


def pgfacility_update(request, pg_id):
    pd = pgdetails.objects.get(pg_id=pg_id)
    form = pgdetailsForm(request.POST, instance=pd)

    print("-----", form.errors)
    if form.is_valid():
        try:
            form.save()
            return redirect("/pgfacility")
        except:
            print("-----", sys.exc_info())
    else:

        return render(request, "pgfacility_edit.html", {"pd": pd})




