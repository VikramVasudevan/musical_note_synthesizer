import functools
import sys
import pygame

print("Welcome to Musical Note Synthesizer!")

# notes = ["S","R","G","M","P","D","N"]
notes = ["s", "r", "g", "p", "d", "S", "R", "G", "P"]
audioMap = [
    "sa lower.mp3",
    "ri.mp3",
    "ga.mp3",
    "pa.mp3",
    "dha.mp3",
    "sa higher.mp3",
    "ri higher.mp3",
    "ga higher.mp3",
    "pa higher.mp3",
]


def playSwaramPattern(prmPattern):
    # Initialize the pygame mixer
    pygame.mixer.init()

    for sequence in prmPattern:
        for swaram in sequence:
            swaramIndex = notes.index(swaram)
            # Load a sound file
            sound_file = "./audio/" + audioMap[swaramIndex]
            sound = pygame.mixer.Sound(sound_file)

            # Play the sound
            sound.play(maxtime=2000, fade_ms=1000)

            # Wait for the sound to finish playing
            # pygame.time.wait(int(sound.get_length() * 1000))
            pygame.time.wait(2000)


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
# pattern = ["s", "p", "g", "r", "s"]
pattern = []
print("This program is designed to teach swaram patterns in carnatic music.")
print("Given the starting pattern from a sequence, the program derives the remaining patterns in the sequence through extrapolation")
print("Additionally, the program creates the mirror image pattern while descending down (avarohanam)")
print("Finally, the program also demonstrates the pattern by singing it for you!")
print("*****Enter each swaram of the pattern followed by a newline. Enter q when done *****")
print("*****For example enter s r g p q (with a newline in between)*****")
for line in sys.stdin:
    if 'q' == line.rstrip():
        break
    if line.rstrip() in notes:
        pattern.append(line.rstrip())
    else:
        raise ("Invalid note")

print("pattern = ", pattern)
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

playSwaramPattern(fullpattern)
