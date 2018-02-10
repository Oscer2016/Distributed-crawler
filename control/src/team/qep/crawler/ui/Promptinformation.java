package team.qep.crawler.ui;

import java.awt.Color;
import java.awt.Font;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;

import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JTextArea;

import team.qep.crawler.util.Constant;

//自定义消息提示框
public class Promptinformation implements MouseListener {
	public static boolean flag=false; //true是   false为否
	private JDialog  infoJD = new JDialog();
	private JPanel infoJP   = new JPanel();
	private JButton  sure  = new JButton();
	private JButton  yes  = new JButton();
	private JButton  no  = new JButton();
	private JTextArea  info = new JTextArea();
				
	public Promptinformation(JFrame jf,String str,int mode){
		flag=false;
    	infoJD = new JDialog(jf,true);
    	this.Init();
		this.setBounds();
		this.setColour();
		this.listener();
		
		infoJP.add(info);
		if(mode==Constant.KeyValue.get("Info")){
			infoJP.add(sure);
		}else if(mode==Constant.KeyValue.get("Confirm")){
			infoJP.add(yes);
			infoJP.add(no);
		}
		info.setText(str);
		
		infoJP.add(info);
		infoJD.add(infoJP);
		infoJD.setVisible(true);
	}

	private void Init() {
		Init.initJDialog(infoJD, "infoJD", Constant.JDialog_Width, Constant.JDialog_Height);
		Init.initJPanel(infoJP, "infoJP");
		
		Init.initJTextArea(info, "info");
		info.setBorder(null);//去掉边框
		info.setEditable(false);//屏蔽输入

		Init.initJButton(sure, "sure");
		Init.initJButton(yes, "yes");
		Init.initJButton(no, "no");
	}

	private void setBounds() {
		infoJP.setBounds(0, 0, Constant.JDialog_Width, Constant.JDialog_Height);
		info.setBounds(25, 35,  Constant.JDialog_Width-50,Constant.JDialog_Height-90);
		sure.setBounds(140, 135, 60, 36);
		yes.setBounds(60, 137, 60, 36);
		no.setBounds(230, 137, 60, 36);
	}

	private void setColour() {
		infoJP.setBackground(Theme.PromptPanelColor);

		info.setFont(new Font("微软雅黑",0,22));
		info.setForeground(Color.black);
		info.setForeground(Color.white);
		info.setOpaque(false);//设为透明
		
		sure.setOpaque(false);
		sure.setBackground(Theme.ButtonColor);
		sure.setIcon(Constant.getIcon(sure,"sureb"));
		yes.setOpaque(false);
		yes.setBackground(Theme.ButtonColor);
		yes.setIcon(Constant.getIcon(yes,"yesb"));
		no.setOpaque(false);
		no.setBackground(Theme.ButtonColor);
		no.setIcon(Constant.getIcon(no,"nob"));
	}

	private void listener() {
		sure.addMouseListener(this);
		yes.addMouseListener(this);
		no.addMouseListener(this);
	}

	public void mouseClicked(MouseEvent e) {// 单击
		if("sure".equals(e.getComponent().getName())){
			infoJD.dispose() ;
	    }else if("yes".equals(e.getComponent().getName())){
	    	Promptinformation.flag=true;
	    	infoJD.dispose();
	    }else if("no".equals(e.getComponent().getName())){
	    	Promptinformation.flag=false;
	    	infoJD.dispose();
	    }
	}

	public void mousePressed(MouseEvent e) {// 按下
		if ("sure".equals(e.getComponent().getName())) {
			sure.setContentAreaFilled(false);
		} else if ("yes".equals(e.getComponent().getName())) {
			yes.setContentAreaFilled(false);
		} else if ("no".equals(e.getComponent().getName())) {
			no.setContentAreaFilled(false);
		} 
	}

	public void mouseReleased(MouseEvent e) {// 释放

	}

	public void mouseEntered(MouseEvent e) {// 进入
		if ("sure".equals(e.getComponent().getName())) {
			sure.setIcon(Constant.getIcon(sure,"surew"));
		} else if ("yes".equals(e.getComponent().getName())) {
			yes.setIcon(Constant.getIcon(yes,"yesw"));
		} else if ("no".equals(e.getComponent().getName())) {
			no.setIcon(Constant.getIcon(no,"now"));
		} 
	}

	public void mouseExited(MouseEvent e) {// 离开
		if ("sure".equals(e.getComponent().getName())) {
			sure.setIcon(Constant.getIcon(sure,"sureb"));
		} else if ("yes".equals(e.getComponent().getName())) {
			yes.setIcon(Constant.getIcon(yes,"yesb"));
		} else if ("no".equals(e.getComponent().getName())) {
			no.setIcon(Constant.getIcon(no,"nob"));
		} 
	}
}
