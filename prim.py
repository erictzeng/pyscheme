def plus(*args):
    return sum(args)

def set_car_bang(cons_pair, new_car):
    cons_pair.car = new_car

def set_cdr_bang(cons_pair, new_cdr):
    cons_pair.cdr = new_cdr

def list(*args):
    if len(args) == 0:
        return NIL
    else:
        return ConsPair(args[0], list(*args[1:]))

def list(*args):
    if len(args) == 0:
        return NIL
    else:
        new_list = ConsPair(args[0], None)
        curr_cons_pair = new_list
        for arg in args[1:]:
            curr_cons_pair.cdr = ConsPair(arg, None)
            curr_cons_pair = curr_cons_pair.cdr
        return new_list
            
    
def append_bang(list1, list2):
    lastPair = None
    currPair = list1
    while True:
        if currPair.cdr = NIL:
            lastPair = currPair
        else:
            currPair = currPair.cdr
    lastPair.cdr = list2

def append(list1, list2):
    new_list = copy.deepycopy(list1)
    append_bang(new_list, list2)
    return new_list
            

def cons(car, cdr):
    return ConsPair(car, cdr)
