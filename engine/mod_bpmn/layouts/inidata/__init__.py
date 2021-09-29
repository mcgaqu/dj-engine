# -*- coding: utf-8 -*-

from . ini_django import get_django_components
from . ini_flutter import get_flutter_components
from . ini_react import get_react_components

def get_components(grade='django'):
    if (grade == 'django'):
        return get_django_components()
    elif (grade == 'flutter'):
        return get_flutter_components()
    elif (grade == 'react'):
        return get_flutter_components()