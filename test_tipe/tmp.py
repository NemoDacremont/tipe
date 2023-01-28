
from manipule_csv import parse_CSV

segmentStatus = parse_CSV("./data/segment_status.csv", remove_header=True, separator=',')
segments = parse_CSV("./data/segments.csv", remove_header=True, separator=',')
streets = parse_CSV("./data/streets.csv", remove_header=True, separator=',')

def maxi_ind(li: list[int]):
	maxi = 0
	ind_maxi = 0
	for i in range(len(li)):
		if li[i] > maxi:
			maxi = li[i]
			ind_maxi = i

	return ind_maxi

def rechercheInd(li: list, itemID: int):
	for i in range(len(li)):
		if li[i][0] == itemID:
			return i

	return -1

def recupereSegmentLePlusPresent(segmentStatus: list):
	vals = [0 for i in range(84536)]

	for i in range(len(segmentStatus)):
		el = segmentStatus[i]

		segmentID = int(el[2])
		vals[segmentID] += 1

	indMaxi = maxi_ind(vals)
	return indMaxi, vals[indMaxi]

def extractSegmentsStatus(segmentStatus: list, segmentID):
	out = []

	for i in range(len(segmentStatus)):
		status = segmentStatus[i]
		if int(status[2]) == segmentID:
			out.append(status)

	return out

def nombreDeSegment(segmentStatus: list, segmentID: int) -> int:
	"""
		Fonction retournant le nombre de segments associés
	"""
	out = 0

	for i in range(len(segmentStatus)):
		if int(segmentStatus[i][2]) == segmentID:
			out += 1

	return out

"""
segmentID, length = recupereSegmentLePlusPresent(segmentStatus)

print(segmentID, length)
print(segments[segmentID])

streetID = int(segments[segmentID][6])
print(streetID)
streetIndex = rechercheInd(streets, streetID)
if streetIndex != -1:
	print(streets[streetIndex])

status = extractSegmentsStatus(segmentStatus, segmentID)

mean = 0
for statu in status:
	print(statu[3])
	mean += int(statu[3])

print(mean / len(status))
"""

def getSegmentsFromStreet(segments: list, streetID: int) -> list[int]:
	out = []

	for i in range(len(segments)):
		segment = segments[i]
		if int(segment[6]) == streetID:
			out.append(segment[0])

	return out

segmentsDico = {}
for segment in segments:
	segmentID = segment[6]
	segmentsDico[segmentID] = segment


vals = {}
for street in streets:
	streetID = int(street[0])
	vals[streetID] = 0
print(len(streets))
for i in range(len(streets)):
	street = streets[i]
	streetID = int(street[0])
	segmentsStreet = getSegmentsFromStreet(segments, int(street[0]))
	#print("segmentStreet", segmentsStreet)

	for segmentID in segmentsStreet:
		segmentID = int(segmentID)
		vals[streetID] += nombreDeSegment(segmentStatus, segmentID)
		#print(nombreDeSegment(segmentStatus, segmentID))

	print(i, vals[streetID])

print(vals)



