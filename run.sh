./runTagger.sh --output-format conll combineddata.txt > postrain.txt
./runTagger.sh --output-format conll DevNoLabels.txt > posdev.txt

python clean.py postrain.txt > cleanPosCombinedData.txt
python clean.py posdev.txt > cleanPosDevNoLabels.txt

./evalit.sh