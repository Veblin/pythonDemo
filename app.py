print('hi')

#
# print('''line1
# line2
# line3''')


# age = 3;
# age = int(input('age is:'));
# if age >= 18:
#     print('age:'+age)
# else:
#     print('teenager')

# SUM NUMBERS
def sum (s,e):
    _sum = s;
    for i in range(e):
        _sum = _sum + i
    print(_sum)

#
# L = ['Bart', 'Lisa', 'Adam']
# for a in L :
#     print(a)

s = int(input('start is :' ))
e = int(input('end is :' ))

sum(s,e);

#cal
def cal(numbers):
    sum = 0
    for i in numbers:
        sum=sum+i*i
    return sum


