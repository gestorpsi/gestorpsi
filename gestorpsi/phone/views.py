from gestorpsi.phone.models import Phone, PhoneType

def phoneList(areas, numbers, exts, types):
    total = len(numbers)
    objs = []
    for i in range(0, total):
        if (len(numbers[i])):
            objs.append(Phone(area=areas[i], phoneNumber=numbers[i], ext=exts[i], phoneType=PhoneType.objects.get(pk=types[i])))
    return objs

def phoneSave(object, areas, numbers, exts, types):
    object.phones.all().delete()
    for phone in phoneList(areas, numbers, exts, types):
        phone.content_object = object
        phone.save()