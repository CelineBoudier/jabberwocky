import os, re, pickle, random

class LanguageProcessing:
  "This class provides methods to process language (eg: detect lang)."
  def __init__(self, sDictionaryPath = "/opt/appu/data/pkl"):
    "The path where the data are stored/to be stored."
    self.sDictionaryPath = sDictionaryPath # TODO : throw an exception if it's not a real path
    self.dDict = {}

  def openDictionary(self, sLanguage):
    if not os.path.isdir(self.sDictionaryPath):
        print(self.sDictionaryPath+" is not a repository!") # TODO : throw error ?
        return
    sFullPath = os.path.join(self.sDictionaryPath, sLanguage.lower()+".pkl")
    if os.path.isfile(sFullPath):
        fPklFile = open(sFullPath, 'rb')
        try:
            dTrigramCorpus = pickle.load(fPklFile)
            try:
                del dTrigramCorpus["TOTAL_WEIGHT"]
            except:
                pass
        except:
            return
        else:
            fPklFile.close()
            self.dDict[sLanguage] = dTrigramCorpus
    else:
        return

  def setDictionaryPath(self, sNewDictionaryPath):
    "If the data path has to be changed."
    self.sDictionaryPath = sNewDictionaryPath # TODO : throw an exception and keep the old value
    if not os.path.isdir(sNewDictionaryPath):
        print(sNewDictionaryPath+" is not a repository")

  def getDictionaryPath(self):
    "Returns the data path."
    return self.sDictionaryPath

  def __sortValues(self, eElem1, eElem2):
    "This private method is a tool for some language processing functions."
    return -cmp(eElem1[1],eElem2[1])

  def generateWord(self, sLanguage, nSize):
    "This function generates a gibberish sLanguage word, of size nSize"
    try:
        dTrigramCorpus = self.dDict[sLanguage]
    except:
        self.openDictionary(sLanguage)
        try:
            dTrigramCorpus = self.dDict[sLanguage]
        except:
            return ""
    sWord = self.chooseTrigram(dTrigramCorpus)
    if len(sWord) >= nSize or len(sWord) < 3:
        return sWord
    else:
      while len(sWord)< nSize:
        try:
            dSubset = {k:dTrigramCorpus[k] for k in dTrigramCorpus.keys() if k.startswith(sWord[-2:])}
            sNew = self.chooseTrigram(dSubset)
        except:
            return sWord
        sWord += sNew[len(sNew)-1]
    return sWord
    

  def chooseTrigram(self, dDict):
    tTrigrams = sorted(dDict.items(), key=lambda x: x[1])
    tTrigrams.reverse()
    dTrigrams = dict(tTrigrams)
    aTrigrams = dTrigrams.keys()
    aFrequ = dTrigrams.values()
    nTotalWeight = sum(aFrequ)
    nTreshold = random.uniform(0, nTotalWeight)
    for i, nWeight in enumerate(aFrequ):
        nTotalWeight -= nWeight
        if nTotalWeight <= nTreshold:
            return aTrigrams[i]

  def createDictionary(self, sStringToProcess):
    "This function creates the trigram dictionary from the input string."
    # Remove uppercase letters and punctuation. Each punctuation character is replaced by a \n.
    sOldCleanString = sStringToProcess.lower()
    sCleanString = re.sub('[ \t\v\f\r]|\d|[!-/:-@[-`{-~]','\n',sOldCleanString)
    #Get all the words
    aString = sCleanString.split('\n')
    dTrigrams = {}
    for sWord in aString:
      if len(sWord) < 4:
        if len(sWord) > 0:
          # The word is a trigram (<= 3 char). Its frequency in the trigram dict is increased.
          try:
            nFreq = dTrigrams[sWord]
          except KeyError:
            dTrigrams[sWord] = 1
          else:
            dTrigrams[sWord] = nFreq + 1
      else:
        # The word contains many trigrams
        nLength = len(sWord)
        nCnt = 0
        while nCnt < nLength - 2:
          sNewTrig = sWord[nCnt:nCnt+3]
          # The frequency of the trigram is increased.
          try:
            nFreq = dTrigrams[sNewTrig]
          except KeyError:
            dTrigrams[sNewTrig] = 1
          else:
            dTrigrams[sNewTrig] = nFreq + 1
          nCnt += 1
    # Returns the trigram dictionary.
    return dTrigrams

  def computeLanguageProbabilities(self, sStringToProcess):
    "Computes the language probabilities for the input string."
    # TODO : optimize the dictionary opening/access

    # Creates the trigram dictionary from the input string.
    dDictionary = self.createDictionary(sStringToProcess)
    if not os.path.isdir(self.sDictionaryPath):
        print(self.sDictionaryPath+" is not a repository!") # TODO : throw error ?
        return
    aDir = os.listdir(self.sDictionaryPath)
    dProb = {}
    # compute the frequency sum of the input trigrams (to normalize)
    rNbrTrigramsInput = sum(dDictionary.values())
    # traversal of the dictionaries
    for sElem in aDir:
        rProba = 0.0
        sLanguage = sElem[:-4]
        try:
            dTrigramCorpus = self.dDict[sLanguage]
        except:
            self.openDictionary(sLanguage)
            try:
                dTrigramCorpus = self.dDict[sLanguage]
            except:
                print "Error while getting " + sLanguage + " dictionary"
                return
        # computes the frequency sum of the learnt trigram dictionary (to normalize)
        rNbrTrigramsCorpus = sum(dTrigramCorpus.values())
        # computes the probability of the current language
        for k, v in dDictionary.iteritems():
            try:
                rCorpusFreq = float(dTrigramCorpus[k])
            except KeyError:
                rCorpusFreq = 0.0
            rProba = rProba + ((rCorpusFreq/float(rNbrTrigramsCorpus)) * (float(v)/ float(rNbrTrigramsInput)))
        dProb[sElem[:len(sElem)-4]]=rProba
    iDic = dProb.items()
    return(iDic)

  def findLanguage(self, sStringToProcess):
    "Returns the name of the most probable language."
    iDic = self.computeLanguageProbabilities(sStringToProcess)
    iDic.sort(self.__sortValues)
    return list(iDic[0])
