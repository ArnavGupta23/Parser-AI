import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# The set of context-free grammar (CFG) rules for parsing sentences
NONTERMINALS = """
S -> PART | PART Conj PART
PART -> NP VP | NP Adv VP | VP

NP -> N | Pro | NA N 
NA -> Det | Adj | NA NA

VP -> V | V SUPP | Adv V SUPP

SUPP -> NP | P NP | Adv | AdvP | SUPP SUPP | SUPP SUPP SUPP
AdvP -> Adv | Adv Conj AdvP | Adv PP

Pro -> "she" | "we"
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    
    # Tokenize the sentence into words using NLTK's word_tokenize function
    tokenized = nltk.tokenize.word_tokenize(sentence)
    # Convert each word to lowercase and filter out any word that does not contain at least one alphabetic character 
    return [c.lower() for c in tokenized if c.isalpha()]



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    
    # Initialize an empty list to store noun phrase chunks
    chunks = []
    # Iterate over all subtrees in the given parse tree
    for subtree in tree.subtrees():
        # If the subtree is labeled NP and does not contain other NP subtrees
        if subtree.label() == "NP" and not any(child.label() == "NP" for child in subtree):
            chunks.append(subtree)
    return chunks



if __name__ == "__main__":
    main()
