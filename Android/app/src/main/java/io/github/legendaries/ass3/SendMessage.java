package io.github.legendaries.ass3;

import android.os.AsyncTask;
import android.util.Log;

import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

public class SendMessage extends AsyncTask<String, Void, Void> {
    private Exception exception;
    @Override
    protected Void doInBackground(String... params) {
        try{
            try{

                Socket socket = new Socket("127.0.0.1", 3600);
                PrintWriter outToServer = new PrintWriter(
                        new OutputStreamWriter(
                                socket.getOutputStream()));

                outToServer.print(params[0]);
                outToServer.flush();

            } catch (IOException e) {
                Log.d("DOESTHISWORK", String.valueOf(e));
            }
        }catch (Exception e){
            Log.d("DOESTHISWORK", String.valueOf(e));
            return null;
        }
        return null;
    }
}

////Executes SendMessage Class
//new SendMessage().execute(editText.getText().toString());
