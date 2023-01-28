
from manipule_csv import parse_CSV
import matplotlib.pyplot as plt

Status = list[str]
SegmentStatusCSV = list[Status]

Segment = list[str]
SegmentsCSV = list[Segment]

Street = list[str]


# format (id, nbDeSegments)
StreetInfo = tuple[int, int]
SegmentStreet = list[StreetInfo]

StreetsCSV = list[Street]

segmentStatusCSV: SegmentStatusCSV = parse_CSV("./data/segment_status.csv", remove_header=True, separator=',')
segments: SegmentsCSV = parse_CSV("./data/segments.csv", remove_header=True, separator=',')
streets: StreetsCSV = parse_CSV("./data/streets.csv", remove_header=True, separator=',')
segmentStreetRaw = parse_CSV("./streetSegments.csv", separator=',')

# Transtype les données en int, pour une facilité d'utilisation pour la suite
segmentStreet: SegmentStreet = []
for segment in segmentStreetRaw:
	el = (int(segment[0]), int(segment[1]))
	segmentStreet.append(el)

# Dico pour la suite
SegmentStatusDico = dict[int, list[Status]]


def maxi_ind(li: list[int] | list[float]) -> int:
	"""
		Retourne l'indice du maximum d'une liste de nombres
	"""
	maxi = 0
	ind_maxi = 0
	for i in range(len(li)):
		if li[i] > maxi:
			maxi = li[i]
			ind_maxi = i

	return ind_maxi


def rechercheInd(li: list, itemID: int) -> int:
	"""
		Recherche l'indice d'un élément ayant pour identifiant itemID, éléments de la forme [itemID, ...]
	"""
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


def extractSegmentsStatus(segmentStatus: SegmentStatusCSV, segmentID: int) -> list[Status]:
	"""
		Retourne la liste des status associés à un segmentID
	"""
	out = []

	for i in range(len(segmentStatus)):
		status = segmentStatus[i]
		if int(status[2]) == segmentID:
			out.append(status)

	return out


def nombreDeSegment(segmentStatus: SegmentStatusCSV, segmentID: int) -> int:
	"""
		Fonction retournant le nombre de segments associés
	"""
	out = 0

	for status in segmentStatus:
		if int(status[2]) == segmentID:
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


def getSegmentsFromStreet(segments: SegmentsCSV, streetID: int) -> list[int]:
	"""
		Retourne les identifiants associés aux segments d'une rue
	"""
	out = []

	for i in range(len(segments)):
		segment = segments[i]
		if int(segment[6]) == streetID:
			out.append(segment[0])

	return out


def velociteMoyenneSegments(segmentStatusDico: SegmentStatusDico, segments: list[Segment]) -> float:
	s = 0
	n = 0
	for segment in segments:
		segmentID = int(segment[0])
		# le segment peut exister sans qu'il n'ait de données associées, il faut donc
		# tester s'il en a:
		if segmentID in segmentStatusDico.keys():
			# somme classique des vélocitées
			for status in segmentStatusDico[segmentID]:
				s += int(status[3])
				n += 1


	return s / n


# liste des segments par rue
segmentsDico = {}
for segment in segments:
	segmentID = int(segment[0])
	segmentsDico[segmentID] = segment

# Associe à un segments tout ses status
segmentStatusDico: SegmentStatusDico = {}
for segmentStatus in segmentStatusCSV:
	segmentID = int(segmentStatus[2])

	if segmentID not in segmentStatusDico.keys():
		segmentStatusDico[segmentID] = []

	segmentStatusDico[segmentID].append(segmentStatus)


# Associe à une rue tout ses segments
StreetSegments = dict[int, list[Segment]]
streetSegments: StreetSegments = {}
for segment in segments:
	streetID = int(segment[6])
	if streetID not in streetSegments.keys():
		streetSegments[streetID] = []
	streetSegments[streetID].append(segment)

"""
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
"""

#
# Calcule la vélocité moyenne de la rue avec le plus de status segments
#

# stocke l'identifiant de la rue et le nombre de segments associés
maxStreet: StreetInfo = segmentStreet[0]

# On cherche le maximum
for street in segmentStreet:
	streetID = street[0]
	nbSegment = street[1]

	if nbSegment > maxStreet[1]:
		maxStreet = street

print("maxStreet:", maxStreet)
print("id:", rechercheInd(streets, maxStreet[0]))

# bout de code récupérant l'indice de la rue
"""
index = -1
for i in range(len(streets)):
	street = streets[i]
	streetID = int(street[0])
	if streetID == maxStreet[0]:
		print("streetindex: ",i)
"""

segmentsDelastreet = streetSegments[maxStreet[0]]

velociteMoyenne = velociteMoyenneSegments(segmentStatusDico, segmentsDelastreet)

print("velocite moyenne:", velociteMoyenne)

cles = segmentStatusDico.keys()
velocites = []
n = 0
for segment in segmentsDelastreet:
	segmentID = int(segment[0])
	# le segment peut exister sans qu'il n'ait de données associées, il faut donc
	# tester s'il en a:
	if segmentID in cles:
		for status in segmentStatusDico[segmentID]:
			velocite = int(status[3])

			velocites.append(velocite)
			if velocite > velociteMoyenne:
				# print(velocite)
				pass


plt.figure()

plt.plot(velocites)

plt.show()

