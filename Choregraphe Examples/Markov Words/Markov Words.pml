<?xml version="1.0" encoding="UTF-8" ?>
<Package name="Markov Words" format_version="4">
    <Manifest src="manifest.xml" />
    <BehaviorDescriptions>
        <BehaviorDescription name="behavior" src="behavior_1" xar="behavior.xar" />
    </BehaviorDescriptions>
    <Dialogs />
    <Resources>
        <File name="text" src="behavior_1/text.txt" />
        <File name="trigrams_markov" src="behavior_1/trigrams_markov.pkl" />
        <File name="words_markov" src="behavior_1/words_markov.pkl" />
        <File name="choice_sentences" src="behavior_1/Aldebaran/choice_sentences.xml" />
    </Resources>
    <Topics />
    <IgnoredPaths>
        <Path src=".metadata" />
    </IgnoredPaths>
</Package>
