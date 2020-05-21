package com.example.py_server_motor_hongjae2;

import android.os.AsyncTask;

import java.net.InetAddress;
import java.net.UnknownHostException;


public class FindAddress extends AsyncTask<Void, Void, String> {
    String domain;
    public FindAddress(String d){
        domain = d;
    }
    @Override
    protected String doInBackground(Void... params) {
        InetAddress inetAddr;
        String ss = "";
        try {
            inetAddr = InetAddress.getByName(domain);
            byte[] addr = inetAddr.getAddress();
            for (int i = 0; i < addr.length; i++) {
                if (i > 0)
                    ss += ".";
                ss += addr[i] & 0xFF;
            }
        } catch (UnknownHostException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        return ss;
    }
}