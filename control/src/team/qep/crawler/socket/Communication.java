package team.qep.crawler.socket;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.ConnectException;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketTimeoutException;
import java.net.UnknownHostException;

import team.qep.crawler.ui.Promptinformation;
import team.qep.crawler.util.Constant;

public class Communication{
	private static final String IP = "120.77.201.150";
	private static final int port = 8888;
	private static String recv = "[]";
	
    public static String SendAndRecv(String send) {
        try{   
        	//1.建立客户端socket连接，指定服务器位置及端口
        	Socket socket = new Socket();
        	InetSocketAddress address=new InetSocketAddress(IP, port);
        	socket.connect(address,3000);//连接超时时长

        	OutputStream os=socket.getOutputStream();
        	PrintWriter pw=new PrintWriter(os);
        	pw.write(send);
        	pw.flush();
        	socket.shutdownOutput();
            System.out.println("主控端:"+send);

        	socket.setSoTimeout(20000);//读数据操作时,最多阻塞10秒钟 时间一到(不再等待读下去了),抛出IOException
        	InputStream is=socket.getInputStream();
        	BufferedReader br=new BufferedReader(new InputStreamReader(is));
        	
            recv=br.readLine();
        	socket.shutdownInput();
            System.out.println("服务端:"+recv);

        	//关闭资源
        	br.close();
        	is.close();
        	pw.close();
        	os.close();
        	socket.close();
        	if(recv==null){
        		new Promptinformation(null, "      很遗憾, 服务器突然崩溃, 是否开除服务器端的程序员?", Constant.KeyValue.get("Confirm"));
        		if(Promptinformation.flag){
        			new Promptinformation(null, "      感谢您的建议, 请尝试重启程序!", Constant.KeyValue.get("Info"));
        			System.exit(0);
        		}else{
        			new Promptinformation(null, "      那还请容忍一会,程序员正努力抢修中!", Constant.KeyValue.get("Info"));
        		}
            }
        } catch (UnknownHostException e) {
        	e.printStackTrace();
        	new Promptinformation(null, "      			未知地址", Constant.KeyValue.get("Info"));
			System.exit(0);
        } catch (ConnectException e) {
        	new Promptinformation(null, "      服务器未打开, 请开启服务器", Constant.KeyValue.get("Info"));
			System.exit(0);
        }catch (SocketTimeoutException e) {
        	e.printStackTrace();
    		new Promptinformation(null, "      很遗憾, 服务器突然崩溃, 是否开除服务器端的程序员?", Constant.KeyValue.get("Confirm"));
    		if(Promptinformation.flag){
    			new Promptinformation(null, "      感谢您的建议, 请尝试重启程序!", Constant.KeyValue.get("Info"));
    			System.exit(0);
    		}else{
    			new Promptinformation(null, "      那还请容忍一会,程序员正努力抢修中!", Constant.KeyValue.get("Info"));
    		}
    	}catch (IOException e) {
        	//服务器未开直接关闭
        	recv="[]";//远程服务器长时间无回响
			e.printStackTrace();
        } 
        return recv;
    }
}