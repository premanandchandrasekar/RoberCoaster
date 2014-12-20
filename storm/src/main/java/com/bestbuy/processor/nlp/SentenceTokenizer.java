package com.bestbuy.processor.nlp;


import opennlp.tools.sentdetect.SentenceDetectorME;
import opennlp.tools.sentdetect.SentenceModel;
import java.io.IOException;
import java.io.InputStream;

public class SentenceTokenizer {
    private static SentenceTokenizer sentenceTokenizer = null;

    private SentenceDetectorME sentenceDetector = null;

    protected SentenceTokenizer(){
        InputStream modelIn = null;
        try {
            modelIn = getClass().getResourceAsStream("/en-sent.bin");
            final SentenceModel sentenceModel = new SentenceModel(modelIn);
            modelIn.close();
            this.sentenceDetector = new SentenceDetectorME(sentenceModel);
        }
        catch (final IOException ioe) {
            ioe.printStackTrace();
        }
        finally {
            if (modelIn != null) {
                try {
                    modelIn.close();
                } catch (final IOException e) {}
            }
        }
    }

    public static  SentenceTokenizer getInstance(){
        if(sentenceTokenizer == null){
          return new SentenceTokenizer();
        }
        return sentenceTokenizer;
    }

    public String[] tokenize(String text){
        return this.sentenceDetector.sentDetect(text);
    }

}
