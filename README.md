jabberwocky
===========

Written Language Detection and Gibberish Synthesis for NAO.


Written Language Detection might be useful for NAO to select the right language for RSS feeds or Web service data of unknown provenance (news, song titles…)

How does it work? Trigrams! I created trigrams frequency lists for English and French (more to come!). So when you write a sentence, the same analysis can be done, and the data compared to the learning data, so NAO can guess the most probable language of the sentence.

Gibberish detection! Since this method is statistical, it works when there are some spelling mistakes, and for English- or French-"looking" gibberish. You can try it on the non-sense poem Jabberwocky by Lewis Carroll! (Unlike hacker's dictionary methods)

Gibberish synthesis! For fun, art, or when NAO doesn't know what to say, you might want him to speak in gibberish. I'm providing a gibberish generator using Markov chains, for words and trigrams (behaviour called Markov Words).
A small Python script also generates anti-texts (texts with words recursively antonimised) :)

Content
=======

Box Library: boxes for your Choregraphe behavior. The library is included in the boxes.
Python: the Python library and the data (English and French) if you want to create your own boxes.
Choregraphe Examples: If you want to know how to use the boxes, please open the examples and test them on your robot!
