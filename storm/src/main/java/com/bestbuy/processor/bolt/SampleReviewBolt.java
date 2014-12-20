package com.bestbuy.processor.bolt;

import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Tuple;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Map;


public class SampleReviewBolt extends BaseRichBolt {
    private OutputCollector _collector;
    private Map conf;

    @Override
    public void prepare(Map conf, TopologyContext topologyContext, OutputCollector outputCollector) {
        this._collector = outputCollector;
        this.conf = conf;
    }

    @Override
    public void execute(Tuple tuple) {
        String text = (String)tuple.getValueByField("text");
        String type = (String)tuple.getValueByField("type");
        String product = (String)tuple.getValueByField("product");
        String date = (String)tuple.getValueByField("date");
        int rating = (Integer)tuple.getValueByField("rating");


        _collector.ack(tuple);
    }

    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declare(new Fields("text", "type"));
    }
}
