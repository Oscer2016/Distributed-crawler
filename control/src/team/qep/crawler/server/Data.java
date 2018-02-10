package team.qep.crawler.server;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Arrays;
import com.csvreader.CsvWriter;

import team.qep.crawler.socket.Communication;
import team.qep.crawler.util.Constant;
import team.qep.crawler.util.ConvertJSON;
import team.qep.crawler.util.StringManipulation;

public class Data {
	//得到运行的任务集
	public static String[][] getRunUrlSet(){
	
		String send=ConvertJSON.toJSON(Constant.Agreement.get("RunUrlSet"),"");
		String[] recv=ConvertJSON.toStringArray(Communication.SendAndRecv(send));
		
		String[][] RunUrlSet=StringManipulation.toTwoDimensionalArrays(recv,6);
		RunUrlSet=StringManipulation.mergeResources(RunUrlSet);//合并机子
		for(int i=0 ; i<RunUrlSet.length; i++){
			for(int j=0 ; j<RunUrlSet[i].length; j++){
				switch(j){
				case 0:RunUrlSet[i][j]=Constant.SupportFuzzyUrl.get(Integer.valueOf(RunUrlSet[i][j]));break;
				case 2:
					if(Integer.valueOf(RunUrlSet[i][j])==Constant.KeyValue.get("E_Commerce")){
						RunUrlSet[i][j]=new String("电商");
					}else if(Integer.valueOf(RunUrlSet[i][j])==Constant.KeyValue.get("Blog")){
						RunUrlSet[i][j]=new String("博客");
					}else if(Integer.valueOf(RunUrlSet[i][j])==Constant.KeyValue.get("News")){
						RunUrlSet[i][j]=new String("新闻");
					}
					break;
				case 5:
					if(Integer.valueOf(RunUrlSet[i][j])==Constant.KeyValue.get("Run")){
						RunUrlSet[i][j]=new String("运行中");
					}else if(Integer.valueOf(RunUrlSet[i][j])==Constant.KeyValue.get("Wait")){
						RunUrlSet[i][j]=new String("暂停中");
					}else if(Integer.valueOf(RunUrlSet[i][j])==Constant.KeyValue.get("Complete")){
						RunUrlSet[i][j]=new String("已完成");
					}
					break;
				}
			}
		}
		return RunUrlSet;		
	}

	//得到所有的任务集
	public static String[][] getALLUrlSet(){
	
		String send=ConvertJSON.toJSON(Constant.Agreement.get("AllUrlSet"),"");
		String[] recv=ConvertJSON.toStringArray(Communication.SendAndRecv(send));
		
		String[][] AllUrlSet=StringManipulation.toTwoDimensionalArrays(recv,2);
		for(int i=0 ; i<AllUrlSet.length; i++){
			AllUrlSet[i][0]=Constant.SupportFuzzyUrl.get(Integer.valueOf(AllUrlSet[i][0]));
		}
		return AllUrlSet;
	}
	//得到即时任务的结果数据   
	public static String[][] getTimelyUrlData() {
		
		String send=ConvertJSON.toJSON(Constant.Agreement.get("TimelyData"),"");
		String[] recv=ConvertJSON.toStringArray(Communication.SendAndRecv(send));
		
		String[][] TimelyData=StringManipulation.toTwoDimensionalArrays(recv,3);
		return TimelyData;
	}
	//存储为文件  参数文件名,文件内容
	public static boolean saveFile(String filename,String content) {
		try {
			File path = new File("./data/BN/");
			if (!path.exists()) {
				path.mkdirs();
			}
			File file = new File("./data/BN/"+filename);
			if (!file.exists()) {
		    	file.createNewFile();
			}
			OutputStreamWriter osw = new OutputStreamWriter(new FileOutputStream(file),"UTF-8");
			osw.write(content);
			osw.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return true;

	}	
	//存储为csv文件  参数----表格名,表头,表格主体
	public static boolean saveCSV(String filename,String[] head,String[][] content) {
		try {
			File path = new File("./data/EC/");
			if (!path.exists()) {
				path.mkdirs();
			}
            CsvWriter csvWriter = new CsvWriter("./data/EC/"+filename,',', Charset.forName("UTF-8"));
            csvWriter.writeRecord(head);
            for(int i=0 ; i<content.length ; i++){
            	csvWriter.writeRecord(content[i]);
            }
            csvWriter.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return true;

	}
	//得到该url对应的数据     keyword为空说明为模糊任务，否则为精确任务
	public static String[][] getUrlData(String url, String keyWord) {
		String[] task = new String[]{String.valueOf(Constant.SupportFuzzyUrl.indexOf(url)),keyWord};
		String content=Arrays.toString(task).substring(1,Arrays.toString(task).length()-1);

		String send=ConvertJSON.toJSON(Constant.Agreement.get("urlData"),content);
		String[] recv=ConvertJSON.toStringArray(Communication.SendAndRecv(send));
	
		String[][] urlData=StringManipulation.toTwoDimensionalArrays(recv,6);
		return urlData;
	}
	//得到进度数据生成折线图
	public static String[][] getScheduleData(String url,String keyWord){
		
		String[] task = new String[]{String.valueOf(Constant.SupportFuzzyUrl.indexOf(url)),keyWord};
		String content=Arrays.toString(task).substring(1,Arrays.toString(task).length()-1);
		String send=ConvertJSON.toJSON(Constant.Agreement.get("ProgressData"),content);
		String[] recv=ConvertJSON.toStringArray(Communication.SendAndRecv(send));

		ArrayList<String[]> list = new ArrayList<String[]>();
		for(int i=1 ; i<recv.length; i+=2){
			list.add(new String[]{recv[i],"任务url: "+url+"        关键字: "+keyWord,recv[i+1]});
		}
		
		String[][] dataSet = new String[list.size()][3];
		for(int i=0 ; i<list.size() ; i++){
			for(int j=0 ; j<3 ; j++){
				dataSet[i][j] = list.get(i)[j];
			}
		}
		StringManipulation.sortByColumn(dataSet,new int[]{2});
		
		return dataSet;
	}	
	//得到下载历史数据(包括终止任务集)
	public static String[][] getDownloadDataSet(){
		String send=ConvertJSON.toJSON(Constant.Agreement.get("DownloadData"),"");
		String[] recv=ConvertJSON.toStringArray(Communication.SendAndRecv(send));
		
		String[][] downloadDataSet=StringManipulation.toTwoDimensionalArrays(recv,3);
		for(int i=0 ; i<downloadDataSet.length; i++){
			downloadDataSet[i][0]=Constant.SupportFuzzyUrl.get(Integer.valueOf(downloadDataSet[i][0]));
		}
		return downloadDataSet;
	}
	//得到总下载量数据生成饼状图
	public static String[][] downloadData(){
	
		String send=ConvertJSON.toJSON(Constant.Agreement.get("TotalData"),"");
		String[] recv=ConvertJSON.toStringArray(Communication.SendAndRecv(send));
	
		ArrayList<String[]> list = new ArrayList<String[]>();
		if(recv.length>3){
			list.add(new String[]{"E-Commerce",recv[1]});
			list.add(new String[]{"Blog",recv[2]});
			list.add(new String[]{"News",recv[3]});
		}
		String[][] dataSet = new String[list.size()][2];
		for(int i=0 ; i<list.size() ; i++){
			for(int j=0 ; j<2 ; j++){
				dataSet[i][j] = list.get(i)[j];
			}
		}
		return dataSet;
	}
	//得到从机资源信息
		public static String[][] getResourceInformation(){
			
			String send=ConvertJSON.toJSON(Constant.Agreement.get("ResourceInformation"),"");
			String[] recv=ConvertJSON.toStringArray(Communication.SendAndRecv(send));
			
			String[][] resource=StringManipulation.toTwoDimensionalArrays(recv,4);
			for(int i=0 ; i<resource.length; i++){
				if(resource[i][2].equals(String.valueOf(Constant.KeyValue.get("Start")))){
					resource[i][2]="工作中";
				}else if(resource[i][2].equals(String.valueOf(Constant.KeyValue.get("Abnormal")))){
					resource[i][2]="终止";
				}else if(resource[i][2].equals(String.valueOf(Constant.KeyValue.get("Stop")))){
					resource[i][2]="未工作";
				}
			}
			return resource;
		}
	//返回有效的从机的数量
	public static int isFfectiveResource(){
		
		int flag=0;
		String send=ConvertJSON.toJSON(Constant.Agreement.get("ResourceInformation"),"");
		String[] recv=ConvertJSON.toStringArray(Communication.SendAndRecv(send));
		
		String[][] resource=StringManipulation.toTwoDimensionalArrays(recv,4);
		for(int i=0 ; i<resource.length; i++){
			if(resource[i][2].equals(String.valueOf(Constant.KeyValue.get("Start")))){
				flag++;
			}
		}
		return flag;
	}
	
	//查找url对应的关键字        参数--->带查找的任务url集(string))    查找的url
	public static String[] getKeyWords(String[][] set,String url) {
		ArrayList<String> list = new ArrayList<String>();
		String[][] taskSet=set;
		for(String[] str:taskSet){
			if(url.equals(str[0])){
				list.add(str[1]);
			}
		}
		return StringManipulation.oneDuplicateRemoval(list.toArray(new String[list.size()]));
	}
}
