package com.bestbuy.processor.util;

import java.math.BigInteger;
import java.security.MessageDigest;
import redis.clients.jedis.Jedis;



public class HashGenerator {

    public static String generateHash(String message) throws Exception{
        String generatedHash = null;
        MessageDigest md5 = MessageDigest.getInstance( "MD5" );
        md5.update(message.getBytes());
        BigInteger hash = new BigInteger( 1, md5.digest() );
        generatedHash = hash.toString(16);
        while ( generatedHash.length() < 32 ) {
            generatedHash = "0" + generatedHash;
        }
        return generatedHash;
    }

    public static Boolean storeHash(Integer project_id, String title_hash, String content_hash, Jedis jedis, int expiration_time){
        //isTitleHash = setRedisHash(project_id, title_hash, jedis, expiration_time);
        return setRedisHash(project_id, content_hash, jedis, expiration_time);
        //Boolean

    }

    private static Boolean setRedisHash(Integer project_id, String hash, Jedis jedis, int expiration_time){
        Boolean isNew = false;
        String key = project_id.toString() + "_" + hash;
        Boolean exists = jedis.hexists(key, hash);
        if(!exists){
            jedis.hset(key, hash, hash);
            jedis.expire(key, expiration_time);
            isNew = true;
        }
        return isNew;
    }
}
