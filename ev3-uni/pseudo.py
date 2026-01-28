
if saw_www:
    streifen += 1
    saw_www = False
    iteration_timer = 0
    if streifen < 0:
        iteration_timer += 1
        if iteration_timer > max_iteration: # barcode active false
            iteration_timer = 0
        elif streifen < 3:
            return "forward"
        elif streifen == 3:
            return "schieben"
        
            
else:
    pass
