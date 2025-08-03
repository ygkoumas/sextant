import math as m

def cos(x):
	return m.cos(x*m.pi/180.0)

def sin(x):
	return m.sin(x*m.pi/180.0)

def cel_to_coord(dec, gha):
	x = -sin(gha)*cos(dec)
	y = sin(dec)
	z = cos(gha)*cos(dec)
	return (x,y,z)

def two_points_angle(dec1, gha1, dec2, gha2):
	p1 = cel_to_coord(dec1, gha1)
	p2 = cel_to_coord(dec2, gha2)
	inner_product = 0
	for i in range(3):
		inner_product += p1[i]* p2[i]
	
	result = 180 * m.acos(inner_product) / m.pi
	degrees = int(result)
	minutes = round((result - degrees) * 60, 2)
	return "{degrees}° {minutes}'".format(degrees=degrees, minutes=minutes)

def transfer_x_axis(theta, point):
	rad_theta = m.pi * theta / 180.0
	matrix = [
		[1, 0, 0],
		[0, m.cos(rad_theta), -m.sin(rad_theta)],
		[0, m.sin(rad_theta), m.cos(rad_theta)],
	]
	return [sum([m[i]*point[i] for i in range(3)]) for m in matrix]
	
		

def two_points_direction(dec_comp, gha_comp, dec_zenith, gha_zenith):
	# we transfer the celestial coordinates
	# computed goes to 0 gha without affecting the calculations
	# zenith moves accordingly
	dec_zenith_transfered = dec_zenith
	gha_zenith_transfered = gha_zenith - gha_comp
	dec_comp_transfered = dec_comp
	gha_comp_transfered = 0
	# change coordinates system to xyz
	# x happens to be matching the local chart of the area of computed point
	zenith_3d = cel_to_coord(dec_zenith_transfered, gha_zenith_transfered)
	comp_3d = cel_to_coord(dec_comp_transfered, gha_comp_transfered)
	# Rx(θ) = | 1  0        0       |
    #         | 0  cos(θ)  -sin(θ)  |
    #         | 0  sin(θ)   cos(θ)  |
	# so we get the new coordinates and we rest ...
	zt = transfer_x_axis(dec_comp_transfered, zenith_3d)
	ct = transfer_x_axis(dec_comp_transfered, comp_3d)
	

	# calculate the angle from zenith to computed position
	# the angle is in anticlockwise math convention
	#### angle = m.atan(zenith_transfered[1]/zenith_transfered[0])
	steepness = (ct[1] - zt[1])/(ct[0] - zt[0])
	angle = m.atan(steepness)
	angle = angle *180.0/m.pi
	if ct[0] < zt[0]:
		angle += 180
	# convert to navigation degrees
	# clockwise and starting from north
	direction = 90 - angle
	if direction < 0:
		direction += 360

	return direction

print(two_points_direction(37.76, -23.417, 51.5, 0))
print(two_points_direction(0, 0, 0, -179))
print(two_points_direction(10, 0, 10, -179))
print(two_points_direction(10, -179, 10, 0))
print(two_points_direction(1, 0, 1, -179))
print(two_points_direction(1, -179, 1, 0))

print(two_points_angle(37.76, -23.417, 51.5, 0))



print(two_points_direction(19.99, -10.50968, 17.3203, -118.06406))
