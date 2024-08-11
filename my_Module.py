
print('this is my moudule its not imported.......')

test_strng = 'will try to test this string var....|'

def find_Index(to_Search,target):
    print('inside test function')
    for i, value in enumerate(to_Search):
         if value==target:
              return i
         
         
    return -1
