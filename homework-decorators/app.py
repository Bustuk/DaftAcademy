Napisz dekorator @to_list,  który opakowuje funkcję zwracającą tekst (iterable)
oraz zwraca jej znaki (elementy) w postaci jednowymiarowej listy.

def to_list(func):
  def iter():
    x=func()
    result=[]
    for element in x:
      result.append(element)
    return result
  return iter
  
Napisz dekorator @is_correct,  który opakowuje funkcję zwracającą słownik. 
Dekorator ma sprawdzić czy w słowniku znajdują się klucze zawarte w argumentach dekoratora. 
Jeśli tak niech zwróci ten słownik, jeśli nie, niech zwraca wartość None.

def is_correct(*args):
    list=[]
    for element in args:
        list.append(element)
    def wrap(func):
        def wrapped():
            x=func()
            result=True
            for element in list:
                if element not in x.keys():
                    result=False
                    break
                else:
                    continue
            return x if result==True else None
        return wrapped
    return wrap
    
    Model answear:
    
    def is_correct(*d_args):
    def wrap(func):
        def wrapped_f(*args, **kwargs):
            result = func(*args, **kwargs)
            for arg in d_args:
                try:
                    result[arg]
                except KeyError:
                    return None
            return result
        return wrapped_f
    return wrap
    
Napisz dekorator @add_date,  który opakowuje funkcję zwracającą słownik. 
Dekorator ma dodać aktualną datę do zwracanego przez dekorowaną funkcję słownika w formacie podanym jako argument dekoratora.
Użyj modułu datetime korzystając z datetime.datetime.now() do pobrania aktualnej daty.

import datetime

def add_date(format):
    def wrap(func):
        def wrapped():
            result=func()
            data = datetime.datetime.now()
            result['date']=datetime.datetime.strftime(data, format)
            return result
        return wrapped
    return wrap
