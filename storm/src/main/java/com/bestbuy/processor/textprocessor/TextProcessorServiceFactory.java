package com.bestbuy.processor.textprocessor;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.TException;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TFramedTransport;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


import java.util.Map;

public class TextProcessorServiceFactory {
    private static final Logger logger = LoggerFactory.getLogger(TextProcessorServiceFactory.class.getSimpleName());
    public static final String TEXT_PROCESSOR_HOST = "textprocessor.host";
    public static final String TEXT_PROCESSOR_PORT = "textprocessor.port";

    public static TextProcessor.Client getServiceClient(Map conf){
        try {

            String host = (String) conf.get(TextProcessorServiceFactory.TEXT_PROCESSOR_HOST);
            Long port = (Long) conf.get(TextProcessorServiceFactory.TEXT_PROCESSOR_PORT);
            TFramedTransport transport;

            logger.info("Connecting to Thrift service on {}:{}", host, port.intValue());

            transport = new TFramedTransport(new TSocket(host, port.intValue()));
            transport.open();
            TProtocol protocol = new TBinaryProtocol(transport);
            TextProcessor.Client client = new TextProcessor.Client(protocol);

            return client;

        }catch (TException x) {
            x.printStackTrace();
            return  null;
        }
    }

    public static void disconnectClient(TextProcessor.Client client){
        client.getInputProtocol().getTransport().close();
    }


}
