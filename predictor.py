import pickle
import nltk
import re
import pandas as pd
from collections import Counter

from nltk import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
from sklearn.svm._libsvm import predict
from spellchecker import SpellChecker
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
stop_words = set(stopwords.words('english'))
additional_stop_words = {"ab", "able", "about", "above", "abst", "ac", "accordance", "according", "accordingly",
                         "across", "act", "actually", "ad", "added", "adj", "ae", "af", "affected", "affecting",
                         "affects", "after", "afterwards", "ag", "again", "against", "ah", "ain", "ain't", "aj", "al",
                         "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always",
                         "am", "among", "amongst", "amoungst", "amount", "an", "and", "announce", "another", "any",
                         "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "ao",
                         "ap", "apart", "apparently", "appear", "appreciate", "appropriate", "approximately", "ar",
                         "are", "aren", "arent", "aren't", "arise", "around", "as", "a's", "aside", "ask", "asking",
                         "associated", "at", "au", "auth", "av", "available", "aw", "away", "awfully", "ax", "ay", "az",
                         "b", "ba", "back", "bc", "bd", "be", "became", "because", "become", "becomes", "becoming",
                         "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind",
                         "being",
                         "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "bi", "bill",
                         "biol", "bj", "bk", "bl", "bn", "both", "bottom", "bp", "br", "brief", "briefly", "bs", "bt",
                         "bu", "but", "bx", "by", "c", "c1", "c2", "c3", "ca", "call", "came", "can", "cannot", "cant",
                         "can't", "cause", "causes", "cc", "cd", "ce", "certain", "certainly", "cf", "cg", "ch",
                         "changes", "ci", "cit", "cj", "cl", "clearly", "cm", "c'mon", "cn", "co", "com", "come",
                         "comes", "con", "concerning", "consequently", "consider", "considering", "contain",
                         "containing", "contains", "corresponding", "could", "couldn", "couldnt", "couldn't", "course",
                         "cp", "cq", "cr", "cry", "cs", "c's", "ct", "cu", "currently", "cv", "cx", "cy", "cz", "d",
                         "d2", "da", "date", "dc", "dd", "de", "definitely", "describe", "described", "despite",
                         "detail", "df", "di", "did", "didn", "didn't", "different", "dj", "dk", "dl", "do", "does",
                         "doesn", "doesn't", "doing", "don", "done", "don't", "down", "downwards", "dp", "dr", "ds",
                         "dt", "du", "due", "during", "dx", "dy", "e", "e2", "e3", "ea", "each", "ec", "ed", "edu",
                         "ee",
                         "ef", "effect", "eg", "ei", "eight", "eighty", "either", "ej", "el", "eleven", "else",
                         "elsewhere", "em", "empty", "en", "end", "ending", "enough", "entirely", "eo", "ep", "eq",
                         "er",
                         "es", "especially", "est", "et", "et-al", "etc", "eu", "ev", "even", "ever", "every",
                         "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except",
                         "ey",
                         "f", "f2", "fa", "far", "fc", "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find",
                         "fire", "first", "five", "fix", "fj", "fl", "fn", "fo", "followed", "following", "follows",
                         "for", "former", "formerly", "forth", "forty", "found", "four", "fr", "from", "front", "fs",
                         "ft", "fu", "full", "further", "furthermore", "fy", "g", "ga", "gave", "ge", "get", "gets",
                         "getting", "gi", "give", "given", "gives", "giving", "gj", "gl", "go", "goes", "going", "gone",
                         "got", "gotten", "gr", "greetings", "gs", "gy", "h", "h2", "h3", "had", "hadn", "hadn't",
                         "happens", "hardly", "has", "hasn", "hasnt", "hasn't", "have", "haven", "haven't", "having",
                         "he", "hed", "he'd", "he'll", "hello", "help", "hence", "her", "here", "hereafter", "hereby",
                         "herein", "heres", "here's", "hereupon", "hers", "herself", "hes", "he's", "hh", "hi", "hid",
                         "him", "himself", "his", "hither", "hj", "ho", "home", "hopefully", "how", "howbeit",
                         "however",
                         "how's", "hr", "hs", "http", "hu", "hundred", "hy", "i", "i2", "i3", "i4", "i6", "i7", "i8",
                         "ia", "ib", "ibid", "ic", "id", "i'd", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il",
                         "i'll", "im", "i'm", "immediate", "immediately", "importance", "important", "in", "inasmuch",
                         "inc", "indeed", "index", "indicate", "indicated", "indicates", "information", "inner",
                         "insofar", "instead", "interest", "into", "invention", "inward", "io", "ip", "iq", "ir", "is",
                         "isn", "isn't", "it", "itd", "it'd", "it'll", "its", "it's", "itself", "iv", "i've", "ix",
                         "iy",
                         "iz", "j", "jj", "jr", "js", "jt", "ju", "just", "k", "ke", "keep", "keeps", "kept", "kg",
                         "kj",
                         "km", "know", "known", "knows", "ko", "l", "l2", "la", "largely", "last", "lately", "later",
                         "latter", "latterly", "lb", "lc", "le", "least", "les", "less", "lest", "let", "lets", "let's",
                         "lf", "like", "liked", "likely", "line", "little", "lj", "ll", "ll", "ln", "lo", "look",
                         "looking", "looks", "los", "lr", "ls", "lt", "ltd", "m", "m2", "ma", "made", "mainly", "make",
                         "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely",
                         "mg",
                         "might", "mightn", "mightn't", "mill", "million", "mine", "miss", "ml", "mn", "mo", "more",
                         "moreover", "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu", "much", "mug", "must",
                         "mustn", "mustn't", "my", "myself", "n", "n2", "na", "name", "namely", "nay", "nc", "nd", "ne",
                         "near", "nearly", "necessarily", "necessary", "need", "needn", "needn't", "needs", "neither",
                         "never", "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "no",
                         "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted",
                         "nothing", "novel", "now", "nowhere", "nr", "ns", "nt", "ny", "o", "oa", "ob", "obtain",
                         "obtained", "obviously", "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj", "ok",
                         "okay",
                         "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only", "onto", "oo", "op", "oq",
                         "or", "ord", "os", "ot", "other", "others", "otherwise", "ou", "ought", "our", "ours",
                         "ourselves", "out", "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "p1",
                         "p2", "p3", "page", "pagecount", "pages", "par", "part", "particular", "particularly", "pas",
                         "past", "pc", "pd", "pe", "per", "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed",
                         "please", "plus", "pm", "pn", "po", "poorly", "possible", "possibly", "potentially", "pp",
                         "pq",
                         "pr", "predominantly", "present", "presumably", "previously", "primarily", "probably",
                         "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py", "q", "qj", "qu", "que",
                         "quickly", "quite", "qv", "r", "r2", "ra", "ran", "rather", "rc", "rd", "re", "readily",
                         "really", "reasonably", "recent", "recently", "ref", "refs", "regarding", "regardless",
                         "regards", "related", "relatively", "research", "research-articl", "respectively", "resulted",
                         "resulting", "results", "rf", "rh", "ri", "right", "rj", "rl", "rm", "rn", "ro", "rq", "rr",
                         "rs", "rt", "ru", "run", "rv", "ry", "s", "s2", "sa", "said", "same", "saw", "say", "saying",
                         "says", "sc", "sd", "se", "sec", "second", "secondly", "section", "see", "seeing", "seem",
                         "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious",
                         "seriously", "seven", "several", "sf", "shall", "shan", "shan't", "she", "shed", "she'd",
                         "she'll", "shes", "she's", "should", "shouldn", "shouldn't", "should've", "show", "showed",
                         "shown", "showns", "shows", "si", "side", "significant", "significantly", "similar",
                         "similarly", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm", "sn", "so",
                         "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes",
                         "somewhat", "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify",
                         "specifying", "sq", "sr", "ss", "st", "still", "stop", "strongly", "sub", "substantially",
                         "successfully", "such", "sufficiently", "suggest", "sup", "sure", "sy", "system", "sz", "t",
                         "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc", "td", "te", "tell", "ten", "tends",
                         "tf", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that's",
                         "that've",
                         "the", "their", "theirs", "tommorow", "today", "them", "themselves", "then", "thence", "there",
                         "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere",
                         "theres", "there's", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'd",
                         "they'll", "theyre", "they're", "they've", "thickv", "thin", "think", "third", "this",
                         "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand", "three", "throug",
                         "through", "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to",
                         "together", "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried", "tries",
                         "truly", "try", "trying", "ts", "t's", "tt", "tv", "twelve", "twenty", "twice", "two", "tx",
                         "u", "u201d", "ue", "ui", "uj", "uk", "um", "un", "under", "unfortunately", "unless", "unlike",
                         "unlikely", "until", "unto", "uo", "up", "upon", "ups", "ur", "us", "use", "used", "useful",
                         "usefully", "usefulness", "uses", "using", "usually", "ut", "v", "va", "value", "various",
                         "vd",
                         "ve", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt",
                         "vu", "w", "wa", "want", "wants", "was", "wasn", "wasnt", "wasn't", "way", "we", "wed", "we'd",
                         "welcome", "well", "we'll", "well-b", "went", "were", "we're", "weren", "werent", "weren't",
                         "we've", "what", "whatever", "what'll", "whats", "what's", "when", "whence", "whenever",
                         "when's", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "where's",
                         "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod",
                         "whoever", "whole", "who'll", "whom", "whomever", "whos", "who's", "whose", "why", "why's",
                         "wi", "widely", "will", "willing", "wish", "with", "within", "without", "wo", "won", "wonder",
                         "wont", "won't", "words", "world", "would", "wouldn", "wouldnt", "wouldn't", "www", "x", "x1",
                         "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y", "y2", "yes",
                         "yet", "yj", "yl", "you", "youd", "you'd", "you'll", "your", "youre", "you're", "yours",
                         "yourself", "yourselves", "yesterday", "you've", "yr", "ys", "yt", "z", "zero", "zi", "zz"}
negation_list = {'not', "shouldn't", "won't", "isn't", "didn't", "wasn't", "shan't", "wasn't", "aren't", "don't",
                 "weren't", "mightn't", "mustn't", "needn't", "hasn't", "shouldn't", "haven't", "doesn't", "wouldn't",
                 "couldn't", "hadn't"}
# Remove not from the stop words
stop_words.update(additional_stop_words)
stop_words = list(stop_words - negation_list)

# Define lemmatizer
lemmatizer = WordNetLemmatizer()
# Define spell checker
spell = SpellChecker()


def preprocessing(review):
    # Tokenize review
    tokens = re.findall(r"[A-Za-z]+", review)
    filtered_review = ""
    pos = ""
    review_pos = nltk.pos_tag(tokens)
    for j, token in enumerate(tokens):
        current_token_pos = tag_dict.get((review_pos[j][1][0]), wordnet.NOUN)
        token = token.strip()
        if not token.isupper():
            token = token.lower()
        # Remove stop words & special characters
        if token not in stop_words:
            if current_token_pos == wordnet.VERB or current_token_pos == wordnet.ADV:
                continue
            pos = pos + " " + current_token_pos
            token = lemmatizer.lemmatize(token, current_token_pos)
            token = spell.correction(token)
            filtered_review = filtered_review + " " + token
    return filtered_review


def vectorize(reviews):
    tfidf = TfidfVectorizer(ngram_range=(1, 2))
    tfidf.fit(reviews)
    return tfidf.transform(reviews)


def predict_reviews(reviews):
    SVM = pickle.load(open("models/SVM.pkl", 'rb'))
    processed_reviews = []
    for i, review in enumerate(reviews):
        processed_reviews.append(preprocessing(review["review"].strip()))

    tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=0.01, max_df=0.8)
    tfidf.fit(processed_reviews)
    vectorized = tfidf.transform(processed_reviews)
    ngrams = open("models/ngrams.txt", "r").read().split(",")
    dummy = pd.DataFrame(vectorized.todense(), columns=tfidf.get_feature_names())
    dummy = dummy.reindex(labels=ngrams, axis=1)
    dummy.fillna(0, inplace=True)

    prediction = SVM.predict(dummy).tolist()
    pos_sample = ""
    neg_sample = ""
    neu_sample = ""
    for i in range(len(reviews)):
        if pos_sample != "" and neg_sample != "" and neu_sample != "":
            break
        if pos_sample == "" and prediction[i] == "POSITIVE":
            pos_sample = reviews[i]["review"]
        if neg_sample == "" and prediction[i] == "NEGATIVE":
            neg_sample = reviews[i]["review"]
        if neu_sample == "" and prediction[i] == "NEUTRAL":
            neu_sample = reviews[i]["review"]

    counter = Counter(prediction),
    return {
        "total_count": len(reviews),
        "POSITIVE": counter[0]["POSITIVE"],
        "NEGATIVE": counter[0]["NEGATIVE"],
        "NEUTRAL": counter[0]["NEUTRAL"],
        "pos_sample": pos_sample,
        "neg_sample": neg_sample,
        "neu_sample": neu_sample,
    }
