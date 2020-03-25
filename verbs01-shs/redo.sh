echo "remake mwverbs"
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
echo "remake mwverbs1"
python mwverbs1.py mwverbs.txt mwverbs1.txt
echo "remake shs_verb_filter.txt"
python shs_verb_filter.py ../shs.txt shs_verb_exclude.txt shs_verb_include.txt shs_verb_filter.txt
echo "remake shs_verb_filter_map.txt"
python shs_verb_filter_map.py shs_verb_filter.txt  mwverbs1.txt shs_verb_filter_map.txt
echo "remake shs_preverb1.txt"
python preverb1.py slp1 ../shs.txt shs_verb_filter_map.txt mwverbs1.txt shs_preverb1.txt shs_preverb1_dbg.txt

echo "remake shs_preverb1_deva.txt"
python transcode_preverb1.py deva shs_preverb1.txt shs_preverb1_deva.txt
