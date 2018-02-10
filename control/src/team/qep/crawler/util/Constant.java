package team.qep.crawler.util;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JLabel;

public class Constant {
	//主窗口默认值
	public static String Theme="BlackWhite";
	public static String RefreshInterval="0";

	public static final int JFrame_Width  = 1024;
	public static final int JFrame_Height = 632;
	public static final int JDialog_Width  = 350;
	public static final int JDialog_Height = 180;
	public static final String[] E_CommerceCcolumnNames = new String[]{"商品url","商品名","商品价格","店铺名","店铺url","店铺综合评分"};//电商数据列名
	public static final String[] BlogNewsCcolumnNames = new String[]{"标题","发布时间","类别","标签","阅读人数","正文摘要"};//博客新闻数据列名
	public static final String[] TaskCcolumnNames = new String[]{"URL","关键字","任务类别","所在从机编号","发布时间","任务状态"};//任务数据列名
	public static final String[] HistoricalTaskCcolumnNames = new String[]{"URL","关键字","总数"};//下载数据列名
	public static final String[] ResourceSchedulingCcolumnNames = new String[]{"从机编号","IP","状态","任务数"};//历史任务数据列名

	//刷新间隔时间
	public static final LinkedHashMap<String,String> Refresh  = new LinkedHashMap<String,String>(){
		{
			put("0" ,"   Not Refreshed");
			put("15"," 15 seconds apart");
			put("30"," 30 seconds apart");
			put("60"," 60 seconds apart");
		}
	};
	//UI选项卡的键值对
	public static final HashMap<String, Integer> UIKeyValue = new HashMap<String, Integer>() {
		{
			put("issueTask1", 0);
			put("issueTask2", 2);
			put("resourceScheduling", 4);
			put("taskControl", 6);
			put("dataMonitoring", 8);
			put("dataDisplay", 10);
			put("historyRecord", 12);
			put("helpDescription", 13);
			put("feedback", 15);
			put("setting", 14);
			put("zoom", 16);
			put("close", 18);
		}
	};
	
	//模糊任务集 
	public static final ArrayList<String> SupportFuzzyUrl = new ArrayList<String>(){{
		add("www.taobao.com");
		add("www.tmall.com");
		add("www.jd.com");
		add("www.cnblogs.com");
		add("blog.csdn.net");
		add("blog.sina.com.cn");
		add("blog.51cto.com");
		add("www.chinanews.com");
		add("www.chinadaily.com.cn");
		add("www.eastday.com");
		add("www.huanqiu.com");
		add("news.sina.com.cn");
	}};
	//模糊任务集上电商与博客新闻的分割线
	public static final int division = 3;
	//精确任务集-------模糊任务集的子集
	public static final ArrayList<String> SupportExactUrl = new ArrayList<String>(){{
		add("www.taobao.com");
		add("www.tmall.com");
		add("www.jd.com");
		add("www.cnblogs.com");
		add("blog.csdn.net");
		add("blog.sina.com.cn");
		add("blog.51cto.com");
		add("news.sina.com.cn");
	}};

	//从机资源表
	public static final ArrayList<String> Resource = new ArrayList<String>(){{
		add("101.200.55.43");
		add("47.94.155.238");
		add("47.93.198.31");
	}};
	//协议表
	public static final HashMap<String, Integer> Agreement = new HashMap<String, Integer>() {
		{
			put("RunUrlSet", 1);//运行的任务集合
			put("AllUrlSet", 2);//所有的任务集合
			put("StopUrlSet", 3);//终止的任务集合
			put("fuzzyUrlPublish", 4);//发布模糊任务
			put("exactUrlPublish", 5);//发布精确任务
			put("timelyUrlPublish", 8);//发布即时任务
			put("ModifyTaskStatus", 9);//修改任务状态
			put("DownloadData", 13);//数据统计表的数据量
			put("ProgressData", 21);//进度折线图的数据量
			put("TotalData", 34);//数据统计饼状图数据量
			put("TimelyData", 35);///即时任务的数据量
			put("urlData", 36);//模糊任务与精确任务的数据量
			put("ResourceInformation", 55);//从机资源信息
			put("ModifyResourceStatus", 56);//修改从机状态
			put("AddDeleteResource", 57);//添加或删除从机资源
			put("DeleteTaskData", 89);//删除任务数据
		}
	};
	
	//功能键值对
	public static final HashMap<String, Integer> KeyValue = new HashMap<String, Integer>() {
		{
			put("Fail", -1);//失败
			put("Success",0);//成功
			put("E_Commerce", 1);//电商
			put("Blog", 2);//博客
			put("News", 3);//新闻
			put("Run", 5);//爬取任务运行中
			put("Wait",8);//爬取任务等待中
			put("Complete", 13);//爬取任务已完成
			put("Start", 21);//启用从机
			put("Abnormal", 34);//从机异常
			put("Stop", 55);//终止从机
			put("Add", 56);//增加从机
			put("Delete", 57);//删除从机
			put("EC",1);//即时任务的数据为电商
			put("BN", 0);//即时任务的数据为新闻
			
			put("Info", 89);//信息窗口
			put("Confirm", 144);//确认对话窗口
		}
	};
	
	public static ImageIcon getIcon(JButton jb,String path) {// 得到icon
		return new ImageIcon(jb.getClass().getResource("/image/icon/"+Theme+"/"+ path + ".png"));
	}
	public static ImageIcon getHelpPicturePath(JLabel jl,int layer) {// 得到帮助说明路径
		return new ImageIcon(jl.getClass().getResource("/image/help/"+layer+".jpg"));

	}
	//导出设置
	public static boolean exportSettings () {// 得到主题名
		File file = new File("./.MT");
		BufferedReader reder=null;
		BufferedWriter writer=null;
		try {
			if(!file.exists()){
				file.createNewFile();
				writer = new BufferedWriter(new FileWriter(file));
				writer.write("Theme:\"BlackWhite\"");
				writer.newLine();
				writer.write("RefreshInterval:\"0\"");
				writer.newLine();
				writer.close();
			}
			reder = new BufferedReader(new FileReader(file));
			String str=null;
			str=reder.readLine();
			System.out.println(str);
			Theme=str.substring(str.indexOf("\"")+1, str.lastIndexOf("\""));
			str=reder.readLine();
			RefreshInterval=str.substring(str.indexOf("\"")+1, str.lastIndexOf("\""));
			reder.close();
		} catch (IOException e) {
			e.printStackTrace();
			return false;
		}finally {
			if(reder!=null){
				try {
					reder.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
		return true;
	}
	//导入设置
	public static boolean importSettings (String theme,String refreshInterval) {// 得到主题名
		RefreshInterval = refreshInterval;
		File file = new File("./.MT");
		BufferedWriter writer=null;
		try {
			if(!file.exists()){
				file.createNewFile();
			}
			writer = new BufferedWriter(new FileWriter(file));
			writer.write("Theme:\""+theme+"\"");
			writer.newLine();
			writer.write("RefreshInterval:\""+refreshInterval+"\"");
			writer.newLine();
			writer.close();
		} catch (IOException e) {
			e.printStackTrace();
			return false;
		}finally {
			if(writer!=null){
				try {
					writer.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
		return true;
	}
}