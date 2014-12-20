package com.bestbuy.processor.redis;

import java.util.Map;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;


public class ConnectionFactory {
    private String host;
    private int port;

    private static ConnectionFactory connectionFactory=null;

    private ConnectionFactory(Map conf)
    {
        host = (String) conf.get(RedisConstants.REDIS_HOST);
        port = ((Long) conf.get(RedisConstants.REDIS_PORT)).intValue();
    }

    public JedisPool getConnection() throws Exception
    {
        JedisPool con = null;
        try{
            con = new JedisPool(new JedisPoolConfig(),
                    this.host,
                    this.port);
        }
        catch (Exception e){
            e.printStackTrace();
        }
        return con;
    }

    public static ConnectionFactory getInstance(Map conf)
    {
        if(connectionFactory==null)
        {
            connectionFactory=new ConnectionFactory(conf);
        }
        return connectionFactory;
    }
}
