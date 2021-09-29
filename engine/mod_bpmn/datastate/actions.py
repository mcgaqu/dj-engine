

#============================



def reducer(inistate, action):
    return

def reducer(state, action):
    #  switch action['type']:
    return action.run(state)
    # switch action.alias:
    #     case 'NUEVA':
    #         return action.json
    #     default:
    #         return state

def get_actions():
    return [# alias, tags(params), json:type + payload 
        ['ADD', 'model'],
        ['UPDATE', 'model,object_id'],
        ['DELETE', 'model,object_id'],
        ['SERVIR_PEDIDO', 'pedido_id']
        ['FACTURAR_ALBARAN', 'albaran_id', facturar_albaran]
    ]

def facturar_albaran(albaran_id):
    return {
        type: 'FACTURAR_ALBARAN',
        albaran_id
    }
facturar_albaran.alias = "FACTUAR_ALBARAN
facturar_albaran.tags = "albaran_id"


    return {
        type: 'FACTURAR_ALBARAN',
        payload: {
            albaran_id: albaran_id,
            factura_id: factura_id
        }
    }

def store_add(text,)


AC_NUEVA = {
    'type': 'NUEVA'
    'payload': {},
}


#----------------------
class Store(object):

    def __init__(self):
        self.state = self.dispatch(self.reducer({}, AC_NUEVA))
        return


    def get_state(self):
        return


    def dispatch(self, reducer):
        self.state = reducer(self.state, action)
        return

    def subscribe(self):
        return

store = Store()

