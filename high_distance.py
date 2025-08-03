import math as m

cell_length = 7

def equal_length(string, length):
	return string + ' '*(length-len(string))
	

def d(H,h,f, rd=2):
	a = -1.0/2
	b = H**0.5 - m.tan(f)
	c = -H +h
	delta = b**2 - 4*a*c
	x1 = round(-b + delta**0.5, rd) if delta > 0 else None
	x2 = round(-b - delta**0.5, rd) if delta > 0 else None
	return (x1,x2)



H = 12

new_row = ['h\\\\f']
for f in range(5, 61,5):
	new_row.append(f)

str_row = map(str, new_row)
str_row = map(lambda st: equal_length(st, cell_length), str_row)
print('|'.join(str_row))


for h in [i *10 for i in range(10)]:
#	print("\n")
	new_row = [h]
	for f in range(5, 61,5):
		new_row.append(max(d(H,h,f)))
	str_row = map(str, new_row)
	str_row = map(lambda st: equal_length(st, cell_length), str_row)
	print('|'.join(str_row))

