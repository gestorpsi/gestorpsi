from gestorpsi.place.models import PlaceType, RoomType, Place
from gestorpsi.gcm.models import Plan
from gestorpsi.gcm.models import PaymentType
from gestorpsi.person.models import Person
from gestorpsi.client.models import Client
from gestorpsi.phone.models import Phone, PhoneType
from django.utils.crypto import get_random_string
from gestorpsi.organization.models import Organization
from gestorpsi.admission.models import ReferralChoice as AdmissionChoice
from gestorpsi.service.models import Service, ServiceType, Area
from gestorpsi.address.models import City, State, Country, AddressType, Address
from gestorpsi.document.models import TypeDocument
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

def setup_required_service():
    service_type = ServiceType()
    service_type.name="Tipo de Servico"
    service_type.save()

    area1 = Area()
    area1.area_name = "area 1"
    area1.save()

    organization1 = Organization.objects.get(name=user_stub()["organization"])

    service1 = Service()
    service1.area = area1;
    service1.name = "Servico 1"
    service1.organization = organization1
    service1.service_type = service_type
    service1.save()

    a = AdmissionChoice()
    a.weight = 1
    a.save()

    u = User()
    u.username = "lala12"
    u.password = "1234512678"
    u.is_superuser = True
    u.save()

    person = Person()
    person.name = "nome12"
    person.user = u
    person.nickname = "apelido12"
    person.save()
    person.organization.add(organization1)
    person.save()

def setup_required_client():
    organization1 = Organization.objects.get(name=user_stub()["organization"])

    user = User.objects.create(username="user1", password="password")
    user.save()

    person = Person.objects.create(user=user)
    person.name = "Pessoa"
    person.nickname = "nickname"
    person.organization.add(organization1)
    person.save()

    client = Client()
    client.person = person
    client.idRecord = 2
    client.is_active = False
    client.save()


def setup_required_data():
    country = Country(name='test', nationality='testing')
    country.save()
    place = Place(label='testing place')
    state = State(name='test', shortName='t', country=country)
    state.save()
    city = City(name='test', state=state)
    city.save()

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
    else:
        placeType = PlaceType.objects.get(description='Matriz')

    place.place_type = placeType

    phone_type = PhoneType(description='Recado', pk=2)
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

    address.city = city
    address.content_object = place

    place.save()

def user_stub():
    st = State.objects.get(name="test")
    city = City.objects.get(name="test")
    plan = Plan.objects.all()[0]

    return {
        "address": u'niceaddress',
        "address_number": u'244',
        "city": str(city.id),
        "cpf": u'741.095.117-63',
        "email": u'user15555@gmail.com',
        "name": u'user15555',
        "organization": u'niceorg',
        "password1": u'nicepass123',
        "password2": u'nicepass123',
        "phone": u'45679078',
        "plan": str(plan.id),
        "shortname": u'NICE',
        "state": str(st.id),
        "username": u'user15',
        "zipcode": u'12312-123',
    }

def bad_user_stub():
    return {
        "address": u'niceaddress',
        "address_number": u'244',
        "city": u'2',
        "cpf": u'741.095.117-63',
        "email": u'user15555@gmail.com',
        "name": u'user15555',
        "organization": u'niceorg',
        "password1": u'nicepass123',
        "plan": u'3',
        "password2": u'nicepass1', # different pass
        "phone": u'(55) 5432-4321',
        "shortname": u'NICE',
        "state": u'5',
        "username": u'user15',
        "zipcode": u'12312-123',
    }

def client_stub():

    person = Person.objects.all()[0]
    return {
        "name": person.name,
        "person": person,
        "nickname": u'client',
        "photo": u'foto_do_cliente',
        "is_active": True,
        "nickname": u'client',
        "gender" : 2,
        "comments": u'coments',
    }

def change_client_stub():

    person = Person.objects.all()[0]

    return {
        "name": person.name,
        "person": person,
        "nickname": u'novo_nickname',
        "photo": u'foto_do_cliente',
        "is_active": True,
        "nickname": u'client',
        "gender" : 2,
        "comments": u'coments',
    }
