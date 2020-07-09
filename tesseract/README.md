Tesseract
---------
Tesseract is an open source text recognition (OCR) engine used for parsing screenshots from the game for the village
tools.

https://github.com/tesseract-ocr/tessdoc/blob/master/Home.md

I trained Tesseract for the fonts that Villagers and Heroes utilizes via the following methodology:

    # Download the Tesseract files we will need
    $ git clone https://github.com/tesseract-ocr/langdata_lstm.git
    $ git clone https://github.com/tesseract-ocr/tessdata_best.git
    $ git clone https://github.com/tesseract-ocr/tesseract.git
    
    # Install brew
    $ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    
    # Install additional libraries needed for compiling tesseract
    $ brew reinstall cairo pango icu4c autoconf libffi libarchive libpng
    # Because of my system, I had to do the following uninstall/reinstalls to get it to work with appropriate versions
    $ brew uninstall glib --ignore-dependencies glib
    $ brew reinstall fontconfig
    
    # Add libraries to configuration
    $ export PKG_CONFIG_PATH=\
    $(brew --prefix)/lib/pkgconfig:\
    $(brew --prefix)/opt/libarchive/lib/pkgconfig:\
    $(brew --prefix)/opt/icu4c/lib/pkgconfig:\
    $(brew --prefix)/opt/libffi/lib/pkgconfig:\
    $(brew --prefix)/opt/libpng/lib/pkgconfig
    
    # Compile tesseract to be able to utilize the training tools
    $ cd tesseract
    $ sh autogen.sh
    $ ./configure
    $ make
    $ sudo make install
    $ make training
    $ sudo make training-install

    # Grab the model from the standard english trained data for testing purposes
    $ sh extract_lstm.sh

    # Generate the training data - max is 4000, good is 200
    $ sh generate_training_data.sh 200

    # Evaluate the standard english trained model against our training data
    $ sh eval.sh eng.lstm
    # This comes up with some error rates, which in our case was:
    #  At iteration 0, stage 0, Eval Char error rate=0.35334267, Word error rate=1.4096878
    
    # Train a new model using the standard english trained model as a base with our new fonts - good is 2000 
    $ sh fine_tune.sh 2000
    # Finished! Error rate = 0.09
    
    # Evaluate the effectiveness of the model
    $ sh eval.sh output/vnh_checkpoint
    # At iteration 0, stage 0, Eval Char error rate=0.099786113, Word error rate=0.45074448
    
    # Combine the standard english trained model with the new training and output the new model
    $ sh combine.sh
 
    # Copy the trained data set to wherever the final resting place is and modify the tesseract calls to use "-l vnh"
    $ sudo cp output/vnh.traineddata /opt/local/share/tessdata/vnh.traineddata
