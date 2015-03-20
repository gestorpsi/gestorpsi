"""
Copyright (C) 2008 GestorPsi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

"""
Description:

Create gestorpsi payment types

"""

from gestorpsi.gcm.models.payment import PaymentType
p = PaymentType()
p.id = 1
p.name = 'Teste 1'
p.save()

p  = PaymentType()
p.id = 4
p.name = 'Teste 4'
p.save()