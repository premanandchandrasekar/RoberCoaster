package com.bestbuy.processor.bolt;

/**
 * Created with IntelliJ IDEA.
 * User: Gautam
 * To change this template use File | Settings | File Templates.
 */
import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Tuple;
import com.bestbuy.processor.textprocessor.TextProcessor;
import com.bestbuy.processor.textprocessor.TextProcessorServiceFactory;
import org.apache.thrift.TException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;


public class SentimentClassifierBolt extends BaseRichBolt {
    private static final Logger logger = LoggerFactory.getLogger(SentimentClassifierBolt.class.getSimpleName());
    private OutputCollector _collector;
    private TextProcessor.Client textProcessor;
    private Map conf;

    @Override
    public void prepare(Map conf, TopologyContext topologyContext, OutputCollector outputCollector) {
        this._collector = outputCollector;
        this.conf = conf;
    }

    @Override
    public void execute(Tuple tuple) {
        String text = (String)tuple.getValueByField("text");

        int sentiment = 50;

        try{
            this.textProcessor = TextProcessorServiceFactory.getServiceClient(conf);
            sentiment =  this.textProcessor.infer_sentiment(text);
            System.out.println(text);
            System.out.println(sentiment);
        }catch (TException ex){

                logger.error("Error processing sentence", ex);
        }finally{
            if(this.textProcessor != null)
                TextProcessorServiceFactory.disconnectClient(this.textProcessor);
        }

        _collector.ack(tuple);
    }
    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declare(new Fields("guid"));
    }
}
