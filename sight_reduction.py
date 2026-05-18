import math as m

"""
function signatures:
dec: declination of the celestial body. Positive for North. Negative for South
gha: Greenwich Hour Angle of the celestial body
lat: chosen position latitude. Positive for North. Negative for South
lon: chosen position longitude. Positive for East. Negative for West
zenith_distance: true zenith distance. In other words (90 minus true altitude) or (90 - Ho)
"""

COOR_STEP = 0.01
SMALL_COOR_STEP = 0.001
DIFF_TOLERANCE = 1/60


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
    assert angle >= 0
    degrees = int(angle)
    minutes = abs(round((angle - degrees) * 60, 1))
    return "{degrees}° {minutes}'".format( degrees=degrees, minutes=minutes)

def find_azimuth(dec, gha, lat, lon, zenith_distance):
	azimuth = m.asin(sin(gha-lon)*cos(dec)/cos(90-zenith_distance))*180/m.pi
	return 360-azimuth if lat > 0 else 180+azimuth

def find_potential_points(dec_v, gha_v, lat_v, lon_v, zenith_distance_v):
	sign_map = {
	  'N': 1,
	  'S': -1,
	  'E': 1,
	  'W': -1,
	}

	dec = dec_v[0] + dec_v[1]/60
	dec * sign_map[dec_v[2]]

	gha = gha_v[0] + gha_v[1]/60

	lat = lat_v[0] + lat_v[1]/60
	lat *= sign_map[lat_v[2]]

	lon = lon_v[0] + lon_v[1]/60
	lon *= sign_map[lon_v[2]]

	zenith_distance = zenith_distance_v[0] + zenith_distance_v[1]/60

	result = []


	answer = "distance calculated (90 - Hc): " + format_angle(true_zenith_distance(dec, gha, lat, lon)) + "\n"
	answer += "azimuth (Zn): " + str(find_azimuth(dec, gha, lat, lon, zenith_distance)) + "\n"


	pot_lat = -90
	while pot_lat <= 90:
		pot_lat += COOR_STEP
		pot_distance = true_zenith_distance(dec, gha, pot_lat, lon)
		neighbor_results = []
		while abs(pot_distance - zenith_distance) <= DIFF_TOLERANCE:
			neighbor_results.append([pot_lat, lon])
			pot_lat += SMALL_COOR_STEP
			pot_distance = true_zenith_distance(dec, gha, pot_lat, lon)
		# from the neighboring points pick up the one which is closer to azymuth distance. It is the best estimate from the list.
		if len(neighbor_results) > 0:
			closest_neighbor_result = min(neighbor_results, key=lambda r: abs(true_zenith_distance(dec, gha, r[0], r[1]) - zenith_distance))
			result.append(closest_neighbor_result)


	pot_lon = -180
	while pot_lon <= 180:
		pot_lon += COOR_STEP
		pot_distance = true_zenith_distance(dec, gha, lat, pot_lon)
		neighbor_results = []
		while abs(pot_distance - zenith_distance) <= DIFF_TOLERANCE:
			neighbor_results.append([lat, pot_lon])
			pot_lon += SMALL_COOR_STEP
			pot_distance = true_zenith_distance(dec, gha, lat, pot_lon)
		# from the neighboring points pick up the one which is closer to azymuth distance. It is the best estimate from the list.
		if len(neighbor_results) > 0:
			closest_neighbor_result = min(neighbor_results, key=lambda r: abs(true_zenith_distance(dec, gha, r[0], r[1]) - zenith_distance))
			result.append(closest_neighbor_result)

	# display first the points that are closer to the chosen position, as they are more likely to be usefull for the navigator
	result.sort(key=lambda r: true_zenith_distance(lat, -lon, r[0], r[1]))

	formated_result = [[format_angle(abs(p[0])) , 'N' if p[0]>= 0 else 'S', format_angle(abs(p[1])), 'E' if p[1]>=0 else 'W' ] for p in result]

	answer += "\nPoins that mach azimuth intercept:\n"
	for fr in formated_result:
		answer += "lat: " + fr[0] + fr[1] + ", lon: " + fr[2] + fr[3] + "\n"
	
	return answer



