# -*- coding: utf-8 -*-

import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from .modelbase import ModelBase

class ModelTree(ModelBase):

    parent = models.ForeignKey('self',# limit_choices_to={'nivel':0},
                              on_delete=models.CASCADE,
                              related_name = "children", # "%(class)s_chidren",
                              null=True, blank=True)
    level = models.IntegerField(null=True, blank=True, default=0)

    pos = models.CharField(max_length=150, null=True, blank=True)

    class Meta(ModelBase.Meta):
        abstract = True


    def _getAscendants(self):
        if not self.parent:
            return []
        else:
            try:
                return [self.parent] + self.parent._getAscendants()
            except:
                import pdb; pdb.set_trace()
                pass
            return []
    Ascendants = property(_getAscendants)



    def _get_level(self):
        return len(self.Ascendants)




    def save(self, *args, **kwargs):
        self.level = self._get_level()
        return super(ModelTree, self).save(*args, **kwargs)




class ModelAuxTree(ModelTree): 
    # trunk = model.ForeignKey(Modelo=<modelo al que extiende>)

    valuex = models.JSONField(null=True, blank=True) 
    class Meta(ModelTree.Meta):
        abstract = True 

#======================================

"""
class ModeloArbol(ModeloBase):
    padre = models.ForeignKey('self',# limit_choices_to={'nivel':0},
                              on_delete=models.CASCADE,
                              related_name = "hijos", # "%(class)s_hijos",
                              null=True, blank=True)
    nivel = models.IntegerField(null=True, blank=True, default=0)

    pos = models.CharField(max_length=150, null=True, blank=True)

    #--------------------------
    hijo1 = models.ForeignKey('self', on_delete=models.SET_NULL,
                              related_name="%(class)s_padre",
                               null=True, blank=True)
 
    hnext = models.ForeignKey('self', on_delete=models.SET_NULL,
                              related_name = "%(class)s_hprev",
                               null=True, blank=True)

    EsArbolActivo = True

  
    class Meta(ModeloBase.Meta):
        abstract = True
        ordering = ['pos']
    
    def __str__(self):
        if not self.pos:
            prefijo = self.alias
        else:
            prefijo = self.pos
        return "%s: %s" % (prefijo, self.nombre)


    def natural_key(self):
        # return self.padre.natural_key() + (self.pos,)
        return self.pos


    def ME_num_hijos(self):
        return self.hijos.count()

    #---------------------------
    def MC_alias0(self):
        return "%s" % self.alias if self.nivel==0 else ''
    MC_alias0.short_description = 'Código'
    MC_alias0.admin_order_field = 'alias'

    def MC_alias1(self):
        return "%s" % self.alias if self.nivel==1 else ''
    MC_alias1.short_description = 'Código'
    MC_alias1.admin_order_field = 'alias'

    def MC_nombre(self):
        if self.nivel > 0:
            return "%s" % self.nombre
        else:
            return format_html('<strong>{}</strong>', self.nombre)
    MC_nombre.short_description = 'Nombre'
    MC_nombre.admin_order_field = 'nombre'
    #---------------------------
    # def _getEsArbolActivo(self):
    #     return False
    # EsArbolActivo = property(_getEsArbolActivo)


    def _getRaiz(self):
        if not self.padre:
            return self
        else:
            return self._getRaiz(self.padre)
    Raiz = property(_getRaiz)       


    def _getHermano1(self):
        if not self.padre:
            return None
        else:
            return self.padre.hijo1
    Hermano1 = property(_getHermano1)  

    def _getHermanoMayor(self):
        if not self.Hermano1:
            return None
        else:
            if self == self.padre.hijo1:
                return self
            else:
                hm = self.Hermano1
                if hm.hnext == self:
                    return hm
                else:
                    return hm.hnext._getHermanoMayor()
    HermanoMayor = property(_getHermanoMayor)

    
    def _getEsTerminal(self):
        no_hijo1 = (not self.hijo1) or (self.hijo1 == None)
        no_hnext = (not self.hnext) or (self.hnext == None)
        if no_hijo1 and no_hnext:
            return True
        else:
            return False
    EsTerminal = property(_getEsTerminal) 

    
    def _getEsRaiz(self):
        no_padre = (not self.padre or self.padre == None)
        no_hermano_mayor = (not self.HermanoMayor or self.HermanoMayor == None)
        if no_padre and no_hermano_mayor:
            return True
        return False
    EsRaiz = property(_getEsRaiz)

    def _getEsLibre(self):
        tiene_hijo1 = (self.hijo1 and self.hijo1 != None)
        tiene_hmenor = (self.hnext and self.hnext != None)
        #print "Tiene_hijo1", tiene_hijo1
        #print "Tiene hmenor", tiene_hmenor
        if self.EsRaiz and (not tiene_hijo1) and (not tiene_hmenor):
            return True
        else:
            return False
    EsLibre = property(_getEsLibre)

    def _getAscendentes(self):
        if not self.padre:
            return []
        else:
            try:
                return [self.padre,] + self.padre._getAscendentes()
            except:
                # import pdb; pdb.set_trace()
                pass
            return []
    Ascendentes = property(_getAscendentes)       
    #--------------------------------
    def _get_nivel(self):
        return len(self.Ascendentes)
        
    def _getArbolOrden(self):
        sufijo = self.orden
        for asc in self.Ascendentes:
            sufijo = "%s.%s" % (asc.orden, sufijo)
        return sufijo
    
    def _getPosArbol(self): # malll excede recursividad
        if self.EsRaiz:
            return ""
        if self.padre:
            padre = self.padre
            return "%s.%s" % (padre._getPosArbol(), len(self.HermanosMayores)+1)
        else:
            return "%02d" % len(self.HermanosMayores)+1
    PosArbol = property(_getPosArbol)

    def save(self, *args, **kwargs):
        self.nivel = self._get_nivel()
        # self.alias = self._getArbolOrden()
        self.pos = self._getArbolOrden()  # self._getPosArbol()
        return super(ModeloArbol, self).save(*args, **kwargs)

    def x_save(self, *args, **kwargs):
        if True: # EsArbolActivo:
            return self.save_arbol(*args, **kwargs)
        else:
            return super(ModeloArbol, self).save(*args, **kwargs)
        
    def _getNumHijos(self):
        return self.hijos.count()
    NumHijos = property(_getNumHijos)
    
    def _getPadrino(self):
        if self.padre:
            return self.padre
        elif self.Hermano1:
           return self.Hermano1
        else:
           return None
    Padrino = property(_getPadrino)

    def _getNodoNext(self):
        if self.hijo1:
            return self.hijo1
        elif self.hnext:
            return self.hnext
        return None
    NodeNext = property(_getNodoNext)
    
    def _getNodoPrev(self):
        if self.HermanoMayor:
            return self.HermanoMayor
        elif self.padre:
            return self.padre
        return None
    NodePrev = property(_getNodoPrev)

    def _getHermanosMayores(self):
        if self.HermanoMayor == None:
            return []
        else:
            return [self.HermanoMayor,] + self.HermanoMayor._getHermanosMayores()
    HermanosMayores = property(_getHermanosMayores)

    def _getDescendientes(self):
        if not self.hijo1:
            return []
        else:
            return [self.hijo1,] + self.hijo1._getDescendientes()
    Descendientes = property(_getDescendientes)
    
    def _getHermanosMenores(self):
        if not self.hnext:
            return []
        else:
            return [self.hnext,] + self.hnext._getHermanosMenores()
    HermanosMenores = property(_getHermanosMenores)

    def _getHijos(self):
        if not self.hijo1:
            return []
        else:
            return [self.hijo1,] + self.hijo1.HermanosMenores
    Hijos = property(_getHijos)
    
    def _getRamaEnLista(self):
        # Incluye el nodo de partida
        # import pdb; pdb.set_trace()
        if self.hijo1 and self.hijo1 != None:
            res = [self,] + self.hijo1._getRamaEnLista()
            for x in self.hijo1.HermanosMenores:
                 res += x._getRamaEnLista()
            return res
        else:
            return [self,]
    RamaEnLista = property(_getRamaEnLista)
    

    def _getRamaEnListaAnidada(self):
        # No incluye el nodo inicial (self)
        res = []
        if not self.EsTerminal:
            if self.hijo1 and self.hijo1 != None:
                res = [[self.hijo1, self.hijo1._getRamaEnListaAnidada(),],]
                for x in self.hijo1.HermanosMenores:
                    res += [[x, x._getRamaEnListaAnidada(),],]
        return res
    RamaEnListaAnidada = property(_getRamaEnListaAnidada)

    def _getRamaEnDic(self):
        res = {}
        if self.EsTerminal:
            return res
        else:
            if self.hijo1 and self.hijo1 != None:
                res[self] = self.hijo1._getRamaEnDic()
            for x in self.HermanosMenores:
                res[x] = x._getRamaEnDic()
            return res
    RamaEnDic = property(_getRamaEnDic)


    #===================================
    
    
    def CE_suma_entero(self):
        if self.hijos.count() == 0:
            return 0
        res = self.hijos.aggregate(
            Sum('entero'))['entero__sum']
        if res:
            return res
        else:
            return 0
        #return self.hijos.aggregate(
        #    Sum('entero'))['entero__sum']
    CE_suma_entero.short_description = 'Suma Entero'


    #===========================================================================


    def y_adjuntar(self, nodo, como_hijo1=None, como_hmenor=None):
        if como_hijo1:
            if self.hijo1:
                nodo.hijo1 = self
                # nodo.savex()
            self.hijo1 = nodo
            self.save()
        if como_hmenor:
            if self.hnext:
                nodo.hnext = self
                # nodo.savex()
            self.hnext = nodo
            self.save()
        for x in nodo.RamaEnLista:
            # print nodo.RamaEnLista
            x.savex()
            
    def y_insertar(self, nodo, como_padre=None, como_hmayor=None):
        if self.padre:
            PP = self.padre
            PP.hijo1 = nodo
            PP.save()
        elif self.hermano_mayor:
            hM = self.hermano_mayor
            hM.hnext = nodo
            hM.save()
        if como_padre:
            nodo.hijo1 = self
        elif como_hmayor:
           nodo.hnext = self
        nodo.savex()
        for x in nodo.RamaEnLista:
            # print x, nodo.RamaEnLista
            x.savex()
            
    def y_liberar(self):
        # solo se pueden liberar los nodos sin hijos, liberar previamente a los descendientes
        if self.EsLibre:
            # print "Es Libre", self.alias
            return
        if not self.hijo1 or self.hijo1 == None:
            if self.padre:
                PP = self.padre
                PP.hijo1 = self.hnext
                PP.savex()
                self.hnext = None
                self.savex()
                nodo = PP
                for x in nodo.RamaEnLista:
                    x.savex()
            elif self.hermano_mayor:
                # print "tiene hermano_mayor"
                hM = self.hermano_mayor
                hM.hnext = self.hnext
                hM.savex()
                self.hnext = None
                self.savex()
                nodo = hM
                for x in nodo.RamaEnLista:
                    x.savex()
            else:
                self.hnext = None
                # print "paso por aqui", self.alias, self.hnext
                self.savex()
   
    def y_delete(self):
        if self.CL_arbol_activo:
            if not self.hijo1:
                self.liberar()
                super(ModeloArbol, self).delete()
        else:
            super(ModelTree2, self).delete()
        
    def y_save1(self):
        if self.CL_arbol_activo():
            self.pos = self._getPos()
            self.nivel = len(self.Ascendentes)
        # return super(ModeloArbol, self).save()
        return self.save()


    def CC_nombre_bonito(self):
        x = ("_"*(0*self.nivel))
        return "%s%s._%s" % (x, self.orden[2:], self.nombre)
    CC_nombre_bonito.short_description = 'Título'
    CC_nombre_bonito.admin_order_field = 'orden'
                                           
    
    def _getIndentado(self):
       x = ("&nbsp;"*(3*self.nivel))
       return "%s%s" % (x, self)
    indentado = property(_getIndentado)

    def MU_edit_objeto(self):
        #import pdb; pdb.set_trace()
        if self.id:
            href = "%s%s/%s/%s/change/" % (settings.ROOT_PATH, self._meta.app_label, self._meta.model_name, self.id)
            etiq = "%s" % (self.alias)
            return format_html('<a href="%s"> <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span> %s </a>' % (href, etiq))
        return '--'
    MU_edit_objeto.short_description = 'Código'    
    
    def ME_final(self):
        #import pdb; pdb.set_trace()
        color='gray'    
        if self.ME_num_hijos() == 0:
            return format_html('<span style="color: {};float: left;" class="glyphicon glyphicon-list-alt" aria-hidden="true"></span>', color)
        else:
            return format_html('<span style="color: {};float:left;" class="glyphicon glyphicon-folder-open" aria-hidden="true"></span>',color)
    ME_final.short_description =''

 
class ModeloXArbol(ModeloArbol): 
    # tronco = model.ForeignKey(Modelo=<modelo al que extiende>)

    datox = JSONField(null=True, blank=True) 
    class Meta(ModeloArbol.Meta):
        abstract = True 
    
"""