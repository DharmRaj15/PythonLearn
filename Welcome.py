test_list = ['def','ghi','pqr']

res  = ", ".join(test_list)

print(res)

res = res.replace('g','_').replace('e','g').replace('_','e').split(', ')

print(res)