echo "remake mwverbs"
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
echo "remake mwverbs1"
python mwverbs1.py mwverbs.txt mwverbs1.txt
echo "remake wil_verb_filter.txt"
python wil_verb_filter.py ../wil.txt wil_verb_exclude.txt wil_verb_include.txt wil_verb_filter.txt
echo "remake wil_verb_filter_map.txt"
python wil_verb_filter_map.py wil_verb_filter.txt  mwverbs1.txt wil_verb_filter_map.txt
echo "remake wil_preverb1.txt"
python preverb1.py slp1 ../wil.txt wil_verb_filter_map.txt mwverbs1.txt wil_preverb1.txt

echo "remake wil_preverb1_deva.txt"
python transcode_preverb1.py deva wil_preverb1.txt wil_preverb1_deva.txt
