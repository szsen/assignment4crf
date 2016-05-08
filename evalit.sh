echo "starting feature extraction"
python featureExtraction.py
echo "starting learning"
crfsuite learn -m mymodel combineddata.feats > combineddata.log
echo "starting tagging"
crfsuite tag -m mymodel DevNoLabels.feats > predtags
echo "making kaggle output"
python pred2kaggle.py predtags > OUTPUT.KAGGLE