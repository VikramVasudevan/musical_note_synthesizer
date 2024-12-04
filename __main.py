import functools

print("Welcome to Musical Note Synthesizer!")

# notes = ["S","R","G","M","P","D","N"]
notes = ["s", "r", "g", "p", "d", "S", "R", "G", "P", "D"]


def getNextNote(prmNote):
    currIndex = notes.index(prmNote)
    nextIndex = (currIndex + 1) % len(notes)
    return notes[nextIndex]


def getNextNNotes(prmNote, prmNumSwarams):
    nextNotes = list(prmNote)
    nextNote = prmNote
    for i in range(0, prmNumSwarams - 1):
        nextNote = getNextNote(nextNote)
        nextNotes.append(nextNote)
    return nextNotes


def getNextSequenceForPattern(prmPattern: list):
    return list(map(getNextNote, prmPattern))


def getNextNSequenceForPattern(prmPattern: list, prmNumSequences):
    sequences = list([prmPattern])
    nextSequence = prmPattern
    for i in range(0, prmNumSequences - 1):
        nextSequence = getNextSequenceForPattern(nextSequence)
        sequences.append(nextSequence)
    for n in reversed(sequences):
        # print("n =", n)
        sequences.append(getMirrorImageForPattern(n))
    return sequences


def printPattern(prmPattern: list):
    for seq in prmPattern:
        for swaram in seq:
            print(swaram, end="")
            print(" ", end="    ")
        print("")


def getHighestSwaramInPattern(prmPattern: list):
    indexList = list(map(notes.index, prmPattern))
    return functools.reduce(lambda a, b: a if a > b else b, indexList)


def getLowestSwaramInPattern(prmPattern: list):
    indexList = list(map(notes.index, prmPattern))
    return functools.reduce(lambda a, b: b if a > b else a, indexList)


def getSwaramVectorFromPattern(prmPattern: list):
    vector = list()
    indexList = list(map(notes.index, prmPattern))
    prevIndex = indexList[0]
    for index in indexList:
        vector.append(index - prevIndex)
        prevIndex = index

    return vector


def getSwaramFromDelta(prmSwaram, delta):
    # print(
    #     f"Getting next swaram in sequence for {prmSwaram} with delta {delta}")
    index = notes.index(prmSwaram)
    newIndex = (index + delta) % len(notes)
    # print(notes[newIndex])
    return notes[newIndex]


def getMirrorImageForPattern(prmPattern: list):
    mirrorImage = list()
    highestSwaram = notes[getHighestSwaramInPattern(prmPattern)]
    vector = getSwaramVectorFromPattern(prmPattern)

    # take the highest swaram and apply the vector to derive  the mirror image.
    swaram = highestSwaram
    for i in range(0, len(prmPattern)):
        swaram = getSwaramFromDelta(swaram, vector[i] * -1)
        mirrorImage.append(swaram)
    # print("mirror image = ", mirrorImage)
    return mirrorImage


searchNote = "P"
numSwarams = 4
# print(getNextNote(searchNote) if searchNote in notes else "DOES NOT EXIST")

# print(f"These are the {numSwarams} swarams after {searchNote}")
# print(getNextNNotes(searchNote,numSwarams))
pattern = ["s", "p", "g", "r"]
# print(getNextSequenceForPattern(pattern))
numSequences = 5
fullpattern = getNextNSequenceForPattern(pattern, numSequences)
print(f"{numSequences} sequences of the pattern {pattern}")
printPattern(fullpattern)

# print(getHighestSwaramInPattern(pattern))
# print(getLowestSwaramInPattern(pattern))

# print("Vector = ")
# print(getSwaramVectorFromPattern(pattern))

# print("Mirror Image = ")
# print(getMirrorImageForPattern(pattern))
