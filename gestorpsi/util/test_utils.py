from gestorpsi.place.models import PlaceType, RoomType, Place
from gestorpsi.gcm.models import Plan
from gestorpsi.gcm.models import PaymentType
from gestorpsi.phone.models import Phone, PhoneType
from gestorpsi.address.models import City, State, Country, AddressType, Address
from gestorpsi.document.models import TypeDocument
from django.contrib.contenttypes.models import ContentType

def setup_required_data():
    place = Place(label='testing place')

    if len(PlaceType.objects.all())==0:
        placeType = PlaceType(description='Matriz')
        placeType.save()
        document = TypeDocument(description='CPF')
        document.save()
        a = AddressType(description='Comercial')
        a.save()
        room_type = RoomType()
        room_type.description = 'sala test'
        room_type.save()
        plan = Plan()
        plan.name = 'Teste 1'
        plan.value = 324.00
        plan.duration = 1
        plan.staff_size = 1
        plan.save()
        p = PaymentType()
        p.id = 1
        p.name = 'Teste 1'
        p.save()
        p  = PaymentType()
        p.id = 4
        p.name = 'Teste 4'
        p.save()
        country = Country(name='test', nationality='testing')
        country.save()
        state = State(name='test', shortName='t', country=country)
        state.save()
        city = City(name='test', state=state)
        city.save()
    else:
        placeType = PlaceType.objects.get(description='Matriz')

    place.place_type = placeType

    phone_type = PhoneType(description='Recado')
    phone_type.save()
    content_type_temp = ContentType()
    content_type_temp.save()
    phone = Phone(area='23', phoneNumber='45679078', ext='4444',
                  phoneType=phone_type, content_type=content_type_temp)
    phone.content_object = place
    phone.save()
    address_type = AddressType(description='Home')
    address_type.save()
    address = Address()
    address.addressPrefix = 'Rua'
    address.addressLine1 = 'Rui Barbosa, 1234'
    address.addressLine2 = 'Anexo II - Sala 4'
    address.neighborhood = 'Centro'
    address.zipCode = '12345-123'
    address.addressType = address_type

    country = Country(name='test', nationality='testing')
    country.save()
    state = State(name='test', shortName='t', country=country)
    state.save()
    city = City(name='test', state=state)
    city.save()

    address.city = city
    address.content_object = place

    place.save()

def user_stub():
    return {
        "address": u'niceaddress',
        "address_number": u'244',
        "city": u'3',
        "cpf": u'741.095.117-63',
        "email": u'user15555@gmail.com',
        "name": u'user15555',
        "organization": u'niceorg',
        "password1": u'nicepass123',
        "password2": u'nicepass123',
        "phone": u'(55) 5432-4321',
        "plan": u'2',
        "shortname": u'NICE',
        "state": u'3',
        "username": u'user15',
        "zipcode": u'12312-123',
    }

def bad_user_stub():
    return {
        "address": u'niceaddress',
        "address_number": u'244',
        "city": u'1',
        "cpf": u'741.095.117-63',
        "email": u'user15555@gmail.com',
        "name": u'user15555',
        "organization": u'niceorg',
        "password1": u'nicepass123',
        "password2": u'nicepass1', # different pass
        "phone": u'(55) 5432-4321',
        "plan": u'1',
        "shortname": u'NICE',
        "state": u'1',
        "username": u'user15',
        "zipcode": u'12312-123',
    }
