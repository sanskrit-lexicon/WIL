echo "remake mwverbs"
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
echo "remake mwverbs1"
python mwverbs1.py mwverbs.txt mwverbs1.txt
echo "remake yat_verb_filter.txt"
python yat_verb_filter.py ../yat.txt yat_verb_exclude.txt yat_verb_include.txt yat_verb_filter.txt
echo "remake yat_verb_filter_map.txt"
python yat_verb_filter_map.py yat_verb_filter.txt  mwverbs1.txt yat_verb_filter_map.txt
echo "remake yat_preverb1.txt"
python preverb1.py slp1 ../yat.txt yat_verb_filter_map.txt mwverbs1.txt yat_preverb1.txt yat_preverb1_dbg.txt

