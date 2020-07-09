rm -rf train/*
cp tessdata_best/eng.traineddata tesseract/tessdata/eng.traineddata
tesseract/src/training/tesstrain.sh --fonts_dir fonts \
    --fontlist 'Inknut Antiqua' 'Droid Serif' \
    --lang eng \
    --linedata_only \
    --langdata_dir langdata_lstm \
    --tessdata_dir tesseract/tessdata \
    --save_box_tiff \
    --maxpages $1 \
    --output_dir train
