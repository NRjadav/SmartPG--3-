import hashlib
import random
import sys

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt

from Admin.form import pgownerForm, galleryForm, pgdetailsForm, feedbackForm
from Admin.function import handle_uploaded_file
from Admin.models import user, bookingdetails, pgdetails, pgowner, area, gallery, facility, pgfacility, feedback, \
    inquiry,WeekMenu,DAY_CHOICES

from datetime import date


def pg_index(request):
    u = user.objects.all().count()

    id = request.session['owner_id']
    p = pgdetails.objects.filter(owner_id=id).count()
    b = bookingdetails.objects.filter(pg_id_id__owner_id_id = id).count()

    d1 = date.today()
    f= feedback.objects.filter(pg_id_id__owner_id_id=id,date=d1)

    bd = bookingdetails.objects.filter(pg_id_id__owner_id_id = id,booking_status=0)

    return render(request, "pg_index.html", {"u":u, "b":b, "p":p,"f":f,"bd":bd})

@csrf_exempt
def bookingdetails2(request):
    id=request.session['owner_id']
    p = pgdetails.objects.filter(owner_id=id)
    b = bookingdetails.objects.all()
    if request.method == "POST":
        id = request.POST.get('pgid')
        print("-----------",id)
        b = bookingdetails.objects.filter(pg_id_id = id)
        return render(request, "owner_data.html", {"b": b})
    else:
        return render(request, "owner_bookingdetails2.html", {"b":b, "p":p})


@csrf_exempt
def bookingdetails1(request):
    id = request.session['owner_id']
    p = pgdetails.objects.filter(owner_id=id)
    if request.method == "POST":
        start = request.POST["sd"]
        end = request.POST["ed"]

        start = parse_date(start)
        end = parse_date(end)
        print(start)

        if start < end:


             b=bookingdetails.objects.filter(booking_date__range=[start, end],pg_id__owner_id=id)
             return render(request, "owner_bookingdetails1.html", {"b":b})
        else:
            b = bookingdetails.objects.select_related('pg_id').filter(pg_id__owner_id=id)
            msg = messages.error(request,"start date must be smaller tha end date")
            return render(request, "owner_bookingdetails1.html", {"b":b, "message":msg})
    else:
        b = bookingdetails.objects.select_related('pg_id').filter(pg_id__owner_id=id)

        return render(request, "owner_bookingdetails1.html", {"b":b})


def owner_login(request):
    if request.method == "POST":

        e = request.POST["email"]
        np = request.POST["password"]
        # np = hashlib.md5(p.encode('utf')).hexdigest()
        print("+++++++++++++++++", np)

        val = pgowner.objects.filter(email=e, password=np).count()

        if val == 1:
            val = pgowner.objects.filter(email=e, password=np)
            print("+++++++++++++++++", val)
            for items in val:
                request.session['owner_name'] = items.owner_name
                request.session['owner_id'] = items.owner_id
                request.session['owner_email'] = items.email
                print("----------", val)
                return redirect("/pgowner/pg_index/")

        else:
            messages.error(request, "Invalid username and password")
            return render(request, "owner_login.html")
    else:

            return render(request, "owner_login.html")


def owner_registration(request):
    a = area.objects.all()
    if request.method == "POST":
        form = pgownerForm(request.POST)
        print("--------", form.errors)
        if form.is_valid():
            try:
                print("------------- Before save data ------------")
                newform = form.save(commit=False)
                # newform.password = hashlib.md5(newform.password.encode('utf')).hexdigest()

                newform.save()

                return redirect("/pgowner/owner_login/")
            except:
                print("--------", sys.exc_info())
        else:
            pass
    else:
        form = pgownerForm()
        return render(request, "owner_registration.html", {"form": form, "area": a})

    return render(request, "owner_registration.html", {"form": form, "area": a})



def Send_OTP(request):
    otp1 = random.randint(10000, 99999)

    e = request.POST.get('email')
    print("---------------", e)
    request.session['owner_email'] = e
    obj = user.objects.filter(email=e,is_admin=0).count()

    if obj == 1:
        data = user.objects.filter(email=e,is_admin=0)

        request.session['client_email'] = e

        val = user.objects.filter(email=e).update(otp=otp1, otp_used=0)
        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject, message, email_from, recipient_list)
        return render(request, "password_reset.html")

    else:
        messages.error(request, "Invalid User Name or Password")
        return render(request, "owner_forgot_password.html")


def set_password(request):
    totp = request.POST['otp']
    print("+++++++++++otp_++++++++++++++++++++", totp)
    tpassword = request.POST.get('npass')
    cpassword = request.POST.get('cpass')

    if tpassword == cpassword:
        e = request.session['owner_email']
        val = user.objects.filter(email=e, is_admin=0, otp=totp, otp_used=0).count()

        if val == 1:
            tp = hashlib.md5(tpassword.encode('utf')).hexdigest()
            val = user.objects.filter(email=e, is_admin=0).update(otp_used=1, password=tp)
            return redirect('/pgowner/owner_login/')
        else:
            messages.error(request, 'OTP does not match')
            return render(request, "password_reset.html")
    else:
        messages.error(request, 'New Password & Confirm Password does not match')
        return render(request, "password_reset.html")

    return render(request, "password_reset.html")





def owner_edit(request):
    u = request.session['owner_id']
    po = pgowner.objects.get(owner_id=u)
    a = area.objects.all()
    print("++++++++++++++++++++++++++++++++++++++++++++", po)
    return render(request,"owner_edit.html", {"u": po, "area": a})


def owner_update(request):
    u = request.session['owner_id']
    po = pgowner.objects.get(owner_id =u)
    a = area.objects.all()
    print("++++++++++++++++++++++++++++++++",po)
    if request.method == "POST":
        form = pgownerForm(request.POST, instance=po)
        print("--------", form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect("/pgowner/pg_index/")
            except:
                print("--------", sys.exc_info())
        else:
            return render(request, "owner_edit.html", {"form":form,"u": po, "area": a})

    return render(request, "owner_edit.html", {"u": po,"area":a})


def owner_gallery(request):
    id = request.session['owner_id']
    g = gallery.objects.filter(pg_id=id)
    return render(request, "owner_gallery.html", {'g':g})


def gallery_ins(request):
    id = request.session['owner_id']
    g = gallery.objects.filter(pg_id_id=id)
    p = pgdetails.objects.all()
    if request.method == "POST":
        form = galleryForm(request.POST, request.FILES)
        print("-------", form.errors)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['gallery_name'])
                form.save()
                return redirect('/pgowner/owner_gallery/')
            except:
                print("--------",sys.exc_info())
        else:
            pass
    else:
        form = galleryForm()
        return render(request, "gallery_ins.html",{'form': form, "p": p})

    return render(request, "gallery_ins.html",{'form': form, "p": p})


def user_view(request):
    id = request.session['owner_id']
    u = user.objects.filter()
    return render(request, "owner_user.html", {"user": u})


def owner(request):
    p = pgowner.objects.all()
    return render(request, "owner.html", {"p":p})



def owner_area(request):
    a = area.objects.all()
    return render(request, "owner_area.html", {"area":a})


def owner_facility(request):
    f = facility.objects.all()
    return render(request, "owner_facility.html", {"facility":f})


def owner_pgfacility(request,id=0):
    pf = pgfacility.objects.filter(pg_id_id=id)
    return render(request, "owner_pgfacility.html", {"pf":pf})


def owner_feedback(request):
    fb = feedback.objects.all()
    return render(request,"owner_feedback.html", {"fb":fb})


def owner_bookingdetails(request):
    b = bookingdetails.objects.all()
    return render(request, "owner_bookingdetails.html", {"b":b})


def owner_inquiry(request):
    i = inquiry.objects.all()
    return render(request, "owner_inquiry.html", {"inquiry":i})


def count_report(request):

    sql1 = " SELECT (select user_name from user where user_id = b.user_id_id) as name,  count(*) as booking_id FROM bookingdetails b JOIN user u where b.user_id_id = u.user_id GROUP by user_id_id "

    data = bookingdetails.objects.raw(sql1)

    return render(request, "owner_countreport.html", {"data": data})


def owner_pgowner(request):
    id = request.session['owner_id']
    print(id)
    pd = pgdetails.objects.filter(owner_id=id)  
    print(pd) 
    a = area.objects.all()
    return render(request, "owner_pgdetails.html", {"pd": pd, "a": a})


def owner_pgmenu(request):
    id = request.session['owner_id']
    print(id)
    pd = WeekMenu.objects.filter(pg_id_id=12)  
    print(pd) 
    a = area.objects.all()
    return render(request, "owner_pgmenu.html", {"pd": pd, "a": a})

def owner_pgdetails_insert(request):
    id = request.session['owner_id']
    pd = pgdetails.objects.filter(owner_id=id)
    a=area.objects.all()
    if request.method == "POST":
        form = pgdetailsForm(request.POST,request.FILES )
        print("-------", form.errors)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['img'])
                form.save()
                return redirect("/pgowner/owner_pgowner/")
            except:
                print("-------", sys.exc_info())
        else:
            pass
    else:
        form = pgdetailsForm()
        return render(request, "owner_pgdetails_insert.html", {"form": form,"a":a, "pd":pd})

    return render(request, "owner_pgdetails_insert.html", {"form": form,"a":a, "pd":pd})

def owner_pgmenu_insert(request):
    id = request.session['owner_id']
    pid = pgdetails.objects.filter(owner_id=id)
    print(pid,id)
    if request.POST:
        pg_id=request.POST['pg_id']
        day_id=request.POST['day_id']
        breakfast=request.POST['breakfast']
        lunch=request.POST['lunch']
        dinner=request.POST['dinner']
        print(pg_id,day_id,breakfast,lunch,dinner)
        pid1=pgdetails.objects.get(pg_name=pg_id)
        print(pid1.pg_id)
        WeekMenu.objects.create(pg_id=pid1,day=day_id,breakfast=breakfast,lunch=lunch,dinner=dinner)
            
    return render(request, "owner_pgmenu_insert.html",{"pid":pid,"DAY_CHOICES":DAY_CHOICES})

def owner_pgdetails_edit(request, pg_id):
    pd = pgdetails.objects.get(pg_id=pg_id)
    form = pgdetailsForm(request.POST, instance=pd)
    if request.POST:
        pg_name=request.POST['pg_name']
        pg_type=request.POST['pg_type']
        description=request.POST['description']
       
        if 'img' in request.FILES:
            img=request.FILES['img']
            pd.pg_name=pg_name
            pd.pg_type=pg_type
            pd.description=description
            pd.img=img
            pd.save()
            return redirect("/pgowner/owner_pgowner/")
             
        # print(pg_name,pg_type,description,img)
        pd.pg_name=pg_name
        pd.pg_type=pg_type
        pd.description=description
        # pd.img=img
        pd.save()
    # print("-----", form.errors)
    # if form.is_valid():
    #     try:
    #         form.save()
        return redirect("/pgowner/owner_pgowner/")
    #     except:
    #         print("-----", sys.exc_info())
    # else:

    return render(request, "owner_pgdetails_edit.html", {"pd": pd})


def owner_pgdetails_update(request, pg_id):
    pd = pgdetails.objects.get(pg_id=pg_id)
    form = pgdetailsForm(request.POST, instance=pd)

    print("-----", form.errors)
    if form.is_valid():
        try:
            form.save()
            return redirect("/pgowner/owner_pgowner/")
        except:
            print("-----", sys.exc_info())
    else:

        return render(request, "owner_pgdetails_edit.html", {"pd": pd})


def owner_feedback_insert(request):
    if request.method == "POST":
        form = feedbackForm(request.POST)
        print("-------", form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect("/pgowner/owner_feedback")
            except:
                print("-------", sys.exc_info())
        else:
            pass
    else:
        form = feedbackForm()
        return render(request, "owner_feedback_insert.html", {"form": form})

    return render(request, "owner_feedback_insert.html", {"form": form})


def owner_feedback_edit(request, feedback_id):
    f = feedback.objects.get(feedback_id=feedback_id)
    return render(request, "owner_feedback_edit.html", {"feedback": f})


def owner_feedback_update(request, feedback_id):
    f = feedback.objects.get(feedback_id=feedback_id)
    f.delete()
    return redirect("/pgowner/owner_feedback/")
       

def owner_forgot_password(request):
    return render(request, "owner_forgot_password.html")


def owner_logout(request):

    try:
        del request.session['user_id']
        del request.session['user_name']
        del request.session['email']

    except:
        pass

    return redirect("/pgowner/owner_login/")


def pgdetails_delete(request, pg_id):
    pd = pgdetails.objects.get(pg_id=pg_id)
    pd.delete()
    return redirect("/pgowner/owner_pgowner/")


