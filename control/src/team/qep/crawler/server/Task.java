package team.qep.crawler.server;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

import team.qep.crawler.socket.Communication;
import team.qep.crawler.util.Constant;
import team.qep.crawler.util.ConvertJSON;

public class Task {
	//发布模糊任务                       参数--->(模糊任务url集string,优先度int)
	public static boolean fuzzyUrlPublish(String fuzzyURL,int priority){
		//1---分割为数组同时去掉重复的url
		Set<String> set = new HashSet<String>(Arrays.asList(fuzzyURL.replace(" ", "").split("\n")));
		//2---去掉不支持(错误)的url
		Set<String> support = new HashSet<String>(Constant.SupportFuzzyUrl);
		set.retainAll(support);
		//3---去掉运行中(已经发布过)的url
		ArrayList<String> list = new ArrayList<String>();
		String[][] runUrlSet=Data.getRunUrlSet();//正在运行的任务集
		boolean flag=true;//重复标志
		for(String url:set){
			flag=true;
			for(String[] str: runUrlSet){
				if(url.equals(str[0]) && str[1].equals("")){
					 flag=false;
					 break;
				}
			}
			if(flag){
				list.add(url);
			}
		}
		//得到待发布的模糊任务集
		String[] fuzzyUrlSet=(String[])list.toArray(new String[list.size()]);

		if(fuzzyUrlSet.length>0){//空任务不发送
			//转为url编号
			int[] task = new int[fuzzyUrlSet.length+1];
			for(int i=0 ; i<task.length-1 ; i++){
				task[i]=Constant.SupportFuzzyUrl.indexOf(fuzzyUrlSet[i]);
			}
			task[task.length-1]=priority;//最后一位为任务优先级
			//待转json发送
			String content=Arrays.toString(task).substring(1,Arrays.toString(task).length()-1);
			String send=ConvertJSON.toJSON(Constant.Agreement.get("fuzzyUrlPublish"),content);
			String[] recv = ConvertJSON.toStringArray(Communication.SendAndRecv(send));
			if(recv.length>0){//<0 说明服务器无响应
				if(recv[0].equals(String.valueOf(Constant.Agreement.get("fuzzyUrlPublish"))) && recv[1].equals(String.valueOf(Constant.KeyValue.get("Success")))){
					return true;
				}
			}
		}
		return false;
	}
	//发布精确任务      参数--->(精确任务url(string)  关键字(string)    优先度(int))
	public static boolean exactUrlPublish(String exactURL, String keyWord, int priority){
		String[][] runUrlSet=Data.getRunUrlSet();//正在运行的任务集
		boolean flag=true;//重复标志
		
		for(String[] str: runUrlSet){
			if(exactURL.equals(str[0]) && str[1].equals(keyWord)){//重复
				 flag=false;
				 break;
			}
		}
		if(flag){//未重复
			//转为url编号
			String[] task = new String[3];
			task[0]=String.valueOf(Constant.SupportFuzzyUrl.indexOf(exactURL));//url下标
			task[1]=keyWord;//关键字
			task[2]=String.valueOf(priority);//最后一位为任务优先级
			//待转json发送
			String content=Arrays.toString(task).substring(1,Arrays.toString(task).length()-1);
			String send=ConvertJSON.toJSON(Constant.Agreement.get("exactUrlPublish"),content);
			String[] recv = ConvertJSON.toStringArray(Communication.SendAndRecv(send));
			
			if(recv.length>0){//<0 说明服务器无响应
				if(recv[0].equals(String.valueOf(Constant.Agreement.get("exactUrlPublish"))) && recv[1].equals(String.valueOf(Constant.KeyValue.get("Success")))){
					return true;
				}
			}
		}
		return false;
	}
	//发布及时任务      参数--->(及时任务url集(string)  模板配置(string))
	public static boolean timelyUrlPublish(String timelyURL) {
		//1---分割为数组同时去掉重复的url
		Set<String> set = new HashSet<String>(Arrays.asList(timelyURL.replace(" ", "").split("\n")));
		String[] timelyUrlSet=(String[])set.toArray(new String[set.size()]);
		String content=Arrays.toString(timelyUrlSet).substring(1,Arrays.toString(timelyUrlSet).length()-1);
		String send=ConvertJSON.toJSON(Constant.Agreement.get("timelyUrlPublish"),content);
		String[] recv = ConvertJSON.toStringArray(Communication.SendAndRecv(send));
		
		if(recv.length>0){//<0 说明服务器无响应
			if(recv[0].equals(String.valueOf(Constant.Agreement.get("timelyUrlPublish"))) && recv[1].equals(String.valueOf(Constant.KeyValue.get("Success")))){
				return true;
			}
		}
		return true;
	}
	//更改任务状态       参数---->url(String)  关键字 (int)  任务状态(int)
	public static boolean modifyTaskStatus(String url,String keyWord,int status) {
		String send=ConvertJSON.toJSON(Constant.Agreement.get("ModifyTaskStatus"),Constant.SupportFuzzyUrl.indexOf(url)+","+keyWord+","+status);
		String[] recv=ConvertJSON.toStringArray(Communication.SendAndRecv(send));
		if(recv.length>0){//<0 说明服务器无响应
			if(recv[0].equals(String.valueOf(Constant.Agreement.get("ModifyTaskStatus"))) && recv[1].equals(String.valueOf(Constant.KeyValue.get("Success")))){
				return true;
			}
		}	
		return false;
	}
	//更改从机状态       参数---->从机编号(String)  状态 ---启用或终止(int)
	public static boolean modifyResourceStatus(String number,int status) {
		String send=ConvertJSON.toJSON(Constant.Agreement.get("ModifyResourceStatus"),number+","+status);
		String[] recv=ConvertJSON.toStringArray(Communication.SendAndRecv(send));
		if(recv.length>0){//<0 说明服务器无响应
			if(recv[0].equals(String.valueOf(Constant.Agreement.get("ModifyResourceStatus"))) && recv[1].equals(String.valueOf(Constant.KeyValue.get("Success")))){
				return true;
			}
		}	
		return false;
	}
	//增删从机       参数---->状态add   1/delete  0(int) 增加的ip(String)/删除的从机编号
	public static boolean addDeleteResource(int status,String number) {
		String send=ConvertJSON.toJSON(Constant.Agreement.get("AddDeleteResource"),status+","+number);
		String[] recv=ConvertJSON.toStringArray(Communication.SendAndRecv(send));
		if(recv.length>0){//<0 说明服务器无响应
			if(recv[0].equals(String.valueOf(Constant.Agreement.get("AddDeleteResource"))) && recv[1].equals(String.valueOf(Constant.KeyValue.get("Success")))){
				return true;
			}
		}	
		return false;
	}
	//删除任务数据      参数--->(url(string) 关键字keyWord(string))
	public static boolean deleteTaskData (String url,String keyWord) {
		String send=ConvertJSON.toJSON(Constant.Agreement.get("DeleteTaskData"),Constant.SupportFuzzyUrl.indexOf(url)+","+keyWord);
		String[] recv=ConvertJSON.toStringArray(Communication.SendAndRecv(send));
		if(recv.length>0){//<0 说明服务器无响应
			if(recv[0].equals(String.valueOf(Constant.Agreement.get("DeleteTaskData"))) && recv[1].equals(String.valueOf(Constant.KeyValue.get("Success")))){
				return true;
			}
		}	
		return false;
	}
}
