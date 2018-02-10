package team.qep.crawler.ui;

import java.awt.Color;
import java.awt.Font;

//主题
public class Theme {
	public static Font TitleFont = new Font("微软雅黑", 0, 26);// 标题字体
	public static Font Tablefont = new Font("微软雅黑", 0, 16);// 表格字体
	public static Color TitleColor ;// 标题文字色
	public static Color ButtonColor ;// 主面板按键色
	public static Color mainPanelColor ;// 主面板色
	public static Color Panel1 ;// 丛面板1
	public static Color Panel2 ;// 丛面板2
	public static Color Panel3 ;// 丛面板3
	public static Color Panel4 ;// 丛面板4
	public static Color Panel5 ;// 丛面板5
	public static Color Panel6 ;// 丛面板6
	public static Color Panel7 ;// 丛面板7
	public static Color Panel8 ;// 丛面板8
	public static Color Panel9 ;// 丛面板9
	public static Color PromptPanelColor ;// 提示面板色
	public static Color SidebarPanelColor ;// 侧边栏面板色
	public static Color SidebarButton1;// 侧边栏按钮1的颜色
	public static Color SidebarButton2;// 侧边栏按钮2的颜色
	public static Color SidebarButton3;// 侧边栏按钮3的颜色
	public static Color SidebarButton4 ;// 侧边栏按钮4的颜色
	public static Color SidebarButton5;// 侧边栏按钮5的颜色
	public static Color SidebarButton6;// 侧边栏按钮6的颜色
	public static Color SidebarButton7;// 侧边栏按钮7的颜色
	public static Color SidebarButton8;// 侧边栏按钮8的颜色
	public static Color SidebarButton9 ;// 侧边栏按钮9的颜色

	public static void setTheme(String str) {
		if (str.equals("BlackWhite")) {
			TitleColor = new Color(255, 255, 255);// 标题文字色
			ButtonColor = new Color(160, 160, 160);// 主面板按键色
			mainPanelColor = new Color(25, 25, 25);// 主面板色
			Panel1 = new Color(25, 25, 25); 
			Panel2 = new Color(25, 25, 25);
			Panel3 = new Color(25, 25, 25); 
			Panel4 = new Color(25, 25, 25);
			Panel5 = new Color(25, 25, 25);
			Panel6 = new Color(25, 25, 25);
			Panel7 = new Color(25, 25, 25);
			Panel8 = new Color(25, 25, 25);
			Panel9 = new Color(25, 25, 25); 
			PromptPanelColor=new Color(90, 90, 90);
			SidebarPanelColor = new Color(90, 90, 90);// 侧边栏面板色
			SidebarButton1 = new Color(90, 90, 90);// 侧边栏按钮1的颜色
			SidebarButton2 = new Color(90, 90, 90);// 侧边栏按钮2的颜色
			SidebarButton3 = new Color(90, 90, 90);// 侧边栏按钮3的颜色
			SidebarButton4 = new Color(90, 90, 90);// 侧边栏按钮4的颜色
			SidebarButton5 = new Color(90, 90, 90);// 侧边栏按钮5的颜色
			SidebarButton6 = new Color(90, 90, 90);// 侧边栏按钮6的颜色
			SidebarButton7 = new Color(90, 90, 90);// 侧边栏按钮7的颜色
			SidebarButton8 = new Color(90, 90, 90);// 侧边栏按钮8的颜色
			SidebarButton9 = new Color(90, 90, 90);// 侧边栏按钮9的颜色
		} else if (str.equals("Color")) {
			TitleColor = new Color(255, 255, 255);// 标题文字色
			ButtonColor = new Color(160, 160, 160);// 主面板按键色
			mainPanelColor = new Color(25, 25, 25);// 主面板色
			Panel1 = new Color(30, 144, 255); 
			Panel2 = new Color(69,137,148);
			Panel3 = new Color(117,36,35); 
			Panel4 = new Color(20,68,106);
			Panel5 = new Color(64,116,52);
			Panel6 = new Color(84,57,138);
			Panel7 = new Color(102,4,69);
			Panel8 = new Color(50,50,50);
			Panel9 = new Color(1,1,76); 
			PromptPanelColor=new Color(90, 90, 90);
			SidebarPanelColor = new Color(200,200,200);// 侧边栏面板色
			SidebarButton1 = new Color(200,200,200);// 侧边栏按钮1的颜色
			SidebarButton2 = new Color(200,200,200);// 侧边栏按钮2的颜色
			SidebarButton3 = new Color(200,200,200);// 侧边栏按钮3的颜色
			SidebarButton4 = new Color(200,200,200);// 侧边栏按钮4的颜色
			SidebarButton5 = new Color(200,200,200);// 侧边栏按钮5的颜色
			SidebarButton6 = new Color(200,200,200);// 侧边栏按钮6的颜色
			SidebarButton7 = new Color(200,200,200);// 侧边栏按钮7的颜色
			SidebarButton8 = new Color(200,200,200);// 侧边栏按钮8的颜色
			SidebarButton9 = new Color(200,200,200);// 侧边栏按钮9的颜色
		}
	}
}