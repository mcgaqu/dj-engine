# -*- coding: utf-8 -*-

from rest_framework import routers

from mod_auth.adjango.apirest import UserViewSet, GroupViewSet
# from mod_auth.companies.apirest import CompanyViewSet, CompanyPropViewSet, MenuViewSet, MenuItemViewSet
# from mod_auth.doctypes.apirest import DocTypeViewSet, DocTypePropViewSet

from neod_auth.empresas.apirest import Empresas1ViewSet

from neod_core.clasifclientes.apirest import (
    Zonas1ViewSet, SubZonas1ViewSet
)

from neod_core.clasifarticulos.apirest import (
    Ubicaciones1ViewSet, Familias1ViewSet, Balanzas1ViewSet, Marcas1ViewSet,
    Modelos1ViewSet, Origen1ViewSet, Tallas1ViewSet, Colores1ViewSet,
    TiposMateria1ViewSet, TarifaCab1ViewSet, MargenesCab1ViewSet, MargenesDet1ViewSet
)


from neod_entity.personas.apirest import (
    Clientes1ViewSet, ClientesContacto1ViewSet,
    Tecnicos1ViewSet, Proveedores1ViewSet, Acreedores1ViewSet,
    Usuarios1ViewSet, UsuarioWeb1ViewSet
)


from neod_entity.productos.apirest import (
    Articulos1ViewSet, Articulos1RapidViewSet,
    ArtiProveedor1ViewSet,
    Formatos1ViewSet, TarifaDet1ViewSet,
    Disponibilidad1ViewSet,
)

from neod_make.tareas.apirest import (
    TipoAccion1ViewSet, TipoTareas1ViewSet, Tareas1ViewSet, Acciones1ViewSet
)

from rest_framework.pagination import PageNumberPagination

class PageNumberPagination1(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 10000


router = routers.DefaultRouter()
router.register(r'group', GroupViewSet)
router.register(r'user', UserViewSet)
router.register(r'empresas1', Empresas1ViewSet)

#--------------------------------
router.register(r'zonas1', Zonas1ViewSet)
router.register(r'subzonas1', SubZonas1ViewSet)
#----------------------
router.register(r'clientes1', Clientes1ViewSet)
router.register(r'clientescontacto1', ClientesContacto1ViewSet)
router.register(r'tecnicos1', Tecnicos1ViewSet)
router.register(r'proveedores1', Proveedores1ViewSet)
router.register(r'acreedores1', Acreedores1ViewSet)
router.register(r'usuarios1', Usuarios1ViewSet)
router.register(r'usuarioweb1', UsuarioWeb1ViewSet)

#--------------------------------
router.register(r'ubicaciones1', Ubicaciones1ViewSet)
router.register(r'familias1', Familias1ViewSet)
router.register(r'balanzas1', Balanzas1ViewSet)
router.register(r'marcas1', Marcas1ViewSet)
router.register(r'modelos1', Modelos1ViewSet)
router.register(r'origen1', Origen1ViewSet)
router.register(r'tallas1', Tallas1ViewSet)
router.register(r'colores1', Colores1ViewSet)
router.register(r'tiposmateria1', TiposMateria1ViewSet)
router.register(r'tarifacab1', TarifaCab1ViewSet)
router.register(r'margenescab1', MargenesCab1ViewSet)
router.register(r'margenesdet1', MargenesDet1ViewSet)
#------------------------------
router.register(r'articulos1', Articulos1ViewSet)
router.register(r'articulos1rapid', Articulos1RapidViewSet)
router.register(r'artiproveedor1', ArtiProveedor1ViewSet)
router.register(r'formatos1', Formatos1ViewSet)
router.register(r'tarifadet1', TarifaDet1ViewSet)
router.register(r'disponibilidad1', Disponibilidad1ViewSet)
#----------------------------------
router.register(r'tipoaccion1', TipoAccion1ViewSet)
router.register(r'tipotareas1', TipoTareas1ViewSet)
router.register(r'tareas1', Tareas1ViewSet)
router.register(r'acciones1', Acciones1ViewSet)
