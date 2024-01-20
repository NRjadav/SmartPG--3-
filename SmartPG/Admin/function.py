def handle_uploaded_file(f):
    print("-----",f.name)
    with open('Admin/static/images/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
