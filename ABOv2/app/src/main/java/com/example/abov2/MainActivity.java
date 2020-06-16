package com.example.abov2;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

import android.view.MotionEvent;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetAddress;
import java.net.Socket;
import java.util.concurrent.ExecutionException;

//Video view를 위한 import


public class MainActivity extends AppCompatActivity {

    Socket socket;     //클라이언트의 소켓

    DataInputStream inputStream;
    DataOutputStream outputStream;

    String ip;
    String port;

    String msg = "";

    boolean isConnected = true;

    LinearLayout linear0, linear_logo;
    RelativeLayout relative1;

    TextView recieveText;
    EditText editTextAddress, editTextPort, messageText;
    ImageButton disconnectBtn, connectBtn;
    Button   leftBtn, upBtn, rightBtn, downBtn;

    WebView webView;
    EditText webViewAddress;
    Button webViewButton;

    ImageButton thanksButton;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        linear_logo=(LinearLayout)findViewById(R.id.linear_logo);
        thanksButton=(ImageButton)findViewById(R.id.thanksButton);


        linear0 = (LinearLayout)findViewById(R.id.linear0);
        final LinearLayout.LayoutParams linear0params = (LinearLayout.LayoutParams) linear0.getLayoutParams();
        relative1 = (RelativeLayout)findViewById(R.id.linear1);


        /**
         * 소켓 통신 관련
         */

        messageText = (EditText) findViewById(R.id.messageText);
        messageText.setVisibility(View.GONE); // 홍재 : message text를 보이지 않게 해서 button 외 접근을 막는다.

        connectBtn = (ImageButton) findViewById(R.id.buttonConnect);
        disconnectBtn = (ImageButton) findViewById(R.id.buttonDisconnect);

        /**
         * 2020.05.17
         * DDNS 를 쓸 경우를 위해 ip를 DNS로 부터 받아오는 코드를 사용
         */

        try {
            String url = new com.example.ABO.FindAddress("abo1234.iptime.org").execute().get(); //2020.05.20 URL로 부터 받기
            editTextAddress = (EditText) findViewById(R.id.addressText);
            editTextAddress.setText(url); //2020.05.17 server의 ip를 적어줌
        } catch (ExecutionException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        editTextPort = (EditText) findViewById(R.id.portText);
        editTextPort.setText("9000");

        recieveText = (TextView) findViewById(R.id.textViewReciev);

        leftBtn = (Button) findViewById(R.id.buttonLeft);
        upBtn = (Button) findViewById(R.id.buttonUp);
        rightBtn = (Button) findViewById(R.id.buttonRight);
        downBtn = (Button) findViewById(R.id.buttonDown);


        /**
         * 2020.03.23 최홍재
         * video 재생하기
         */


        webView = (WebView) findViewById(R.id.webView);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.loadUrl("http://abo1234.iptime.org:5000/");
        webView.setWebChromeClient(new WebChromeClient());
        webView.setWebViewClient(new WebViewClientClass());
        webView.getSettings().setBuiltInZoomControls(true);
        webView.getSettings().setSupportZoom(true);



        webViewAddress = (EditText)findViewById(R.id.webViewAddress);
        final String webViewAddr = webViewAddress.getText().toString();

        webViewButton = (Button)findViewById(R.id.webViewButton);
        webViewButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                final String webViewAddr = webViewAddress.getText().toString();
                webView.loadUrl(webViewAddr);

            }
        });




        //connect 버튼 클릭
        connectBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ClientSocketOpen(connectBtn);
                linear0params.topMargin = 0;
                editTextAddress.setVisibility(View.GONE);
                editTextPort.setVisibility(View.GONE);
                webView.setVisibility(View.VISIBLE);
                relative1.setVisibility(View.VISIBLE);
                connectBtn.setVisibility(View.GONE);
                disconnectBtn.setVisibility(View.VISIBLE);
                webViewButton.setVisibility(View.VISIBLE);
                webViewAddress.setVisibility(View.VISIBLE);
                linear_logo.setVisibility(View.GONE);
                thanksButton.setVisibility(View.GONE);
            }
        });



        //left 버튼 클릭
        leftBtn.setOnTouchListener(new View.OnTouchListener() {

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    messageText.setText("left");
                    SendMessage(leftBtn);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    messageText.setText("stop");
                    SendMessage(leftBtn);
                }
                return false;
            }
        });

        //up 버튼 클릭
        upBtn.setOnTouchListener(new View.OnTouchListener() {

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    messageText.setText("up");
                    SendMessage(upBtn);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    messageText.setText("stop");
                    SendMessage(upBtn);
                }
                return false;
            }
        });

        //right 버튼 클릭
        rightBtn.setOnTouchListener(new View.OnTouchListener() {

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    messageText.setText("right");
                    SendMessage(rightBtn);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    messageText.setText("stop");
                    SendMessage(rightBtn);
                }
                return false;
            }
        });

        //down 버튼 클릭
        downBtn.setOnTouchListener(new View.OnTouchListener() {

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    messageText.setText("down");
                    SendMessage(downBtn);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    messageText.setText("stop");
                    SendMessage(downBtn);
                }
                return false;
            }
        });

        //Disconnect 버튼 클릭
        disconnectBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                messageText.setText("END");
                SendMessage(disconnectBtn);
            }
        });

    }

    /**
     * 2020.03.23 최홍재
     * cutomsetting?
     */

    private class WebViewClientClass extends WebViewClient {
        @Override
        public boolean shouldOverrideUrlLoading(WebView view, String url) {
            view.loadUrl(url);
            return true;
        }
    }

    public void ClientSocketOpen(View view) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                // TODO Auto-generated method stub
                try {
                    ip = editTextAddress.getText().toString();//IP 주소가 작성되어 있는 EditText에서 서버 IP 얻어오기
                    port = editTextPort.getText().toString();
                    if (ip.isEmpty() || port.isEmpty()) {
                        MainActivity.this.runOnUiThread(new Runnable() {
                            public void run() {
                                Toast.makeText(MainActivity.this, "ip주소와 포트번호를 입력해주세요.", Toast.LENGTH_SHORT).show();
                            }
                        });
                    } else {
                        //서버와 연결하는 소켓 생성..
                        socket = new Socket(InetAddress.getByName(ip), Integer.parseInt(port));
                        //여기까지 왔다는 것을 예외가 발생하지 않았다는 것이므로 소켓 연결 성공..

                        //서버와 메세지를 주고받을 통로 구축
                        inputStream = new DataInputStream(socket.getInputStream());
                        outputStream = new DataOutputStream(socket.getOutputStream());

                        MainActivity.this.runOnUiThread(new Runnable() {
                            public void run() {
                                Toast.makeText(MainActivity.this, "Connected With Server", Toast.LENGTH_SHORT).show();
                            }
                        });
                    }
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }

                //서버와 접속이 끊길 때까지 무한반복하면서 서버의 메세지 수신
                while (isConnected) {
                    try {
                        msg = inputStream.readUTF(); //서버 부터 메세지가 전송되면 이를 UTF형식으로 읽어서 String 으로 리턴
                        //runOnUiThread()는 별도의 Thread가 main Thread에게 UI 작업을 요청하는 메소드이다
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                // TODO Auto-generated method stub
                                recieveText.setText("서버의 응답 : " + msg);
                            }
                        });
                    } catch (IOException e) {
                        // TODO Auto-generated catch block
                        e.printStackTrace();
                    }
                }//while
            }//run method...
        }).start();//Thread 실행..
    }

    public void SendMessage(View view) {
        if (outputStream == null) return;   //서버와 연결되어 있지 않다면 전송불가..

        //네트워크 작업이므로 Thread 생성
        new Thread(new Runnable() {
            @Override
            public void run() {
                // TODO Auto-generated method stub
                //서버로 보낼 메세지 EditText로 부터 얻어오기
                String msg = messageText.getText().toString();
                try {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            String msg = messageText.getText().toString();
                            // TODO Auto-generated method stub
                            recieveText.setText("서버의 응답 : " + msg);
                        }
                    });
                    outputStream.write(msg.getBytes());  //서버로 메세지 보내기.UTF 방식으로(한글 전송가능...) 홍재 : msg를 string으로 받을 경우 python 서버에서 오류가 발생하므로 Byte로 받는다.
                    outputStream.flush();        //다음 메세지 전송을 위해 연결통로의 버퍼를 지워주는 메소드..

                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }//run method..

        }).start(); //Thread 실행..
    }

    @Override
    protected void onStop() {
        super.onStop();
        try {
            socket.close(); //소켓을 닫는다.
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
