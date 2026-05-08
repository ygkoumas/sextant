import math as m

"""
function signatures:
dec: declination of the celestial body
gha: Greenwich Hour Angle of the celestial body
lat: chosen position latitude
lon: chosen position longitude
zenith_distance: distance calculated from the sextant reading after correcting for all errors to get the altitude Hc, and converting to distance by using the formula: distance = 90 - Hc
"""

def float_range(start, stop, step):
    while start < stop:
        yield start
        start += step

def cos(x):
	return m.cos(x*m.pi/180.0)

def sin(x):
	return m.sin(x*m.pi/180.0)

def cel_to_cartesian(dec, gha):
	x = -sin(gha)*cos(dec)
	y = sin(dec)
	z = cos(gha)*cos(dec)
	return (x,y,z)

def true_zenith_distance(dec, gha, lat, lon):
	p1 = cel_to_cartesian(dec, gha)
	p2 = cel_to_cartesian(lat, -lon)
	inner_product = 0
	for i in range(3):
		inner_product += p1[i]* p2[i]
	
	result = 180 * m.acos(inner_product) / m.pi
	return result

def format_angle(angle):
	degrees = int(angle)
	minutes = abs(round((angle - degrees) * 60, 2))
	return "{degrees}° {minutes}'".format( degrees=degrees, minutes=minutes)

def find_azimuth(dec, gha, lat, lon, zenith_distance):
	azimuth = m.asin(sin(gha-lon)*cos(dec)/cos(90-zenith_distance))*180/m.pi
	return 360-azimuth if lat > 0 else 180+azimuth

def find_potential_points(dec, gha, lat, lon, zenith_distance):
	dec = dec[0] + dec[1]/60
	gha = gha[0] + gha[1]/60
	lat = lat[0] + lat[1]/60
	lon = lon[0] + lon[1]/60
	result = []
	print("distance calculated: " + format_angle(true_zenith_distance(dec, gha, lat, lon)))

	pot_lat = -90
	while pot_lat <= 90:
		pot_lat += 0.1
		pot_distance = true_zenith_distance(dec, gha, pot_lat, lon)
		if abs(pot_distance - zenith_distance) <= 1/60:
			result.append([pot_lat, lon])
			while abs(pot_distance - zenith_distance) <= 1/60:
				pot_lat += 0.01
				pot_distance = true_zenith_distance(dec, gha, pot_lat, lon)


	pot_lon = -180
	while pot_lon <= 180:
		pot_lon += 0.01
		pot_distance = true_zenith_distance(dec, gha, lat, pot_lon)
		if abs(pot_distance - zenith_distance) <= 1/60:
			result.append([lat, pot_lon])
			while abs(pot_distance - zenith_distance) <= 1/60:
				pot_lon += 0.01
				pot_distance = true_zenith_distance(dec, gha, lat, pot_lon)
	formated_result = [[format_angle(p[0]), format_angle(p[1])] for p in result]
	for fr in formated_result:
		print("lat: " + fr[0] + ", lon: " + fr[1])
	
	print("azimuth: " + str(find_azimuth(dec, gha, lat, lon, zenith_distance)))
	return formated_result



