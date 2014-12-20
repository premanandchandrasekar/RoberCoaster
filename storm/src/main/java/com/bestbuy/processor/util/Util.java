package com.bestbuy.processor.util;

import org.apache.commons.codec.binary.Base64;
import org.joda.time.DateTime;
import org.joda.time.Period;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class Util {

    public static boolean isDateWithinDuration(DateTime dateTime, String cutoffDuration) {
        Period p = parsePeriod(cutoffDuration);
        return isDateWithinDuration(dateTime, p);
    }

    public static boolean isDateWithinDuration(DateTime dateTime, Period cutoffPeriod) {
        if(cutoffPeriod == null) {
            return false;
        }

        DateTime cutoffDateTime = DateTime.now().minus(cutoffPeriod);
        return dateTime.isAfter(cutoffDateTime);
    }

    public static Period parsePeriod(String periodString)  {
        Period p = null;

        if(periodString == null || periodString.trim().length() < 2) {
            return p;
        }

        char pType = periodString.substring(periodString.length()-1).charAt(0);

        String pStr = periodString.substring(0, periodString.length()-1);
        Integer pValue = 0;
        try {
            pValue = Integer.parseInt(pStr);
        }
        catch (NumberFormatException e) {}

        if(pValue == 0) {
            return p;
        }

        switch (pType) {
            case 'y':   //year
                p = new Period().plusYears(pValue);
                break;
            case 'M':   //month
                p = new Period().plusMonths(pValue);
                break;
            case 'w':   //week
                p = new Period().plusWeeks(pValue);
                break;
            case 'd':   //week
                p = new Period().plusDays(pValue);
                break;
            case 'h':   //hour
                p = new Period().plusHours(pValue);
                break;
            case 'm':   //minutes
                p = new Period().plusMinutes(pValue);
                break;
            case 's':   //seconds
                p = new Period().plusSeconds(pValue);
                break;
        }

        return p;
    }


    public static Date processDate(String dt) {
        try {

            Date date = new SimpleDateFormat("dd/M/yyyy", Locale.ENGLISH).parse(dt);
            return date;

        } catch (ParseException e) {
            return null;
        }
    }


    public static float processRating(String rating) {
        int maxrating = 5;
        float res = 0;

        if (rating.contains("/")) {
            String[] parts = rating.split("/");
            res = Float.parseFloat(parts[0]) / Float.parseFloat(parts[1]);

        } else {
            res = Float.parseFloat(rating);
        }

        if (res * maxrating > maxrating)
            res = 0;

        return res;
    }

    public static String processLocation(String loc) {
        return loc.toLowerCase();
    }
}
