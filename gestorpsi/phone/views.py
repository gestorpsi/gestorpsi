from gestorpsi.phone.models import Phone, PhoneType

# Check if phone fields are equals
def is_equal(phone):
    try:
        phone_db = Phone.objects.get(pk=phone.id)
    except:
        return False
    if cmp(phone_db, phone) == 0:
        return True
    else:
        return False

# Create a phone's list, but don't append blank phone numbers 
def phone_list(ids, areas, numbers, exts, types): 
    objs = []
    for i in range(0, len(numbers)):
        if (len(numbers[i])):
            objs.append(Phone(id=ids[i], area=areas[i], phoneNumber=numbers[i], ext=exts[i], phoneType=PhoneType.objects.get(pk=types[i])))
    return objs

# 'number' field blank means that it was deleted by an user
# So, if len(number) == 0 AND len(id) != 0, delete phone using id
def phone_delete(ids, numbers): 
    for i in range(0, len(numbers)):
        if (not len(numbers[i]) and len(ids[i])):
            Phone.objects.get(pk=ids[i]).delete()

def phone_save(object, ids, areas, numbers, exts, types):
    phone_delete(ids, numbers)
    for phone in phone_list(ids, areas, numbers, exts, types):
        if not is_equal(phone):
            phone.content_object = object
            phone.save()