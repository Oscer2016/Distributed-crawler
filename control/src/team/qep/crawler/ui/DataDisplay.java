package team.qep.crawler.ui;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextArea;
import javax.swing.table.DefaultTableModel;
import team.qep.crawler.server.Data;
import team.qep.crawler.util.Constant;
import team.qep.crawler.util.StringManipulation;

public class DataDisplay extends JPanel implements MouseListener, ActionListener {
	private boolean flag = true;// true---电商 false---新闻博客
	private int  page = 0;//文章总页数

	private JLabel dataDisplay = new JLabel("数   据   展   示");

	private JComboBox<String> selectUrl = new JComboBox<String>();  //选择url(模糊or电商)
	private JComboBox<String> selectKeyword  = new JComboBox<String>(); //选择关键字
	private JButton dataDisplayRefresh = new JButton();// 刷新
	private String[][] data;
	private DefaultTableModel ecDataModel;
	private JTable ecDataJT = new JTable();
	private JScrollPane ecDataJSP = new JScrollPane(ecDataJT); // 未终止的任务数据集

	private JButton upper = new JButton();// 上一篇
	private JButton lower = new JButton();// 下一篇
	private JTextArea bnDataJTA = new JTextArea();
	private JScrollPane bnDataJSP = new JScrollPane(bnDataJTA); //新闻博客数据视图

	public DataDisplay() {
		this.Init();
		this.loadingData();
		this.setBounds();
		this.setColour();
		this.listener();

		this.add(dataDisplay);
		this.add(selectUrl);
		this.add(selectKeyword);
		this.add(dataDisplayRefresh);
		
		this.add(ecDataJSP);
	}

	private void loadingData() {// 装载数据
		ecDataModel = new DefaultTableModel(new String[0][], Constant.E_CommerceCcolumnNames){
			public void setValueAt(Object aValue, int row, int column){}
		};
		ecDataJT.setModel(ecDataModel);
	}

	private void Init() {
		Init.initJLable(dataDisplay, "dataDisplay");

		Init.initJComboBox(selectUrl, "selectUrl");
		Init.initJComboBox(selectKeyword, "selectKeyword");
		Init.initJButton(dataDisplayRefresh, "dataDisplayRefresh");
		
		Init.initJButton(upper, "upper");
		Init.initJButton(lower, "lower");
		Init.initJTable(ecDataJT, "ecDataJT");
		Init.initJScrollPane(ecDataJSP, "ecDataJSP");
		Init.initJTextArea(bnDataJTA, "bnDataJTA");
		Init.initJScrollPane(bnDataJSP, "bnDataJSP");
	}

	private void setBounds() {
		dataDisplay.setBounds(320, 0, 300, 35);
		selectUrl.setBounds(130, 55, 200, 33);
		selectKeyword.setBounds(430,55, 150, 33);
		dataDisplayRefresh.setBounds(695, 51, 150, 40);
		
		ecDataJSP.setBounds(20, 120, 934, 450);
		upper.setBounds(20, 260,50,140);
		bnDataJSP.setBounds(85, 120, 804, 450);
		lower.setBounds(904, 260,50,140);
	}

	private void setColour() {
		this.setBackground(Theme.Panel7);

		dataDisplay.setFont(Theme.TitleFont);
		dataDisplay.setForeground(Theme.TitleColor);
		dataDisplayRefresh.setBackground(Theme.ButtonColor);
		dataDisplayRefresh.setIcon(Constant.getIcon(dataDisplayRefresh,"dataDisplayRefresh"));
		upper.setBackground(Theme.ButtonColor);
		upper.setIcon(Constant.getIcon(upper,"upper"));
		lower.setBackground(Theme.ButtonColor);
		lower.setIcon(Constant.getIcon(lower,"lower"));
		ecDataJT.setFont(Theme.Tablefont);// 设置字体格式
		bnDataJTA.setEditable(false);//屏蔽输入
//		bnDataJTA.setLineWrap(false);
		bnDataJTA.setFont(Theme.Tablefont);
	}

	private void listener() {
		selectUrl.addActionListener(this);
		selectKeyword.addActionListener(this);
		dataDisplayRefresh.addMouseListener(this);
		upper.addMouseListener(this);
		lower.addMouseListener(this);
	}

	public void actionPerformed(ActionEvent e) {
		if (e.getSource() == selectUrl) {
			selectKeyword.removeAllItems();
			if(selectUrl.getItemCount()>0){
				for(String str:Data.getKeyWords(Data.getALLUrlSet(),selectUrl.getSelectedItem().toString())){
					selectKeyword.addItem(str);
				}
			}
		}else if(e.getSource() == selectKeyword) {
			if(selectKeyword.getItemCount()>0){
				this.remove(upper);
				this.remove(lower);
				this.remove(ecDataJSP);
				this.remove(bnDataJSP);
				String url = selectUrl.getSelectedItem().toString();
				String keyWord = selectKeyword.getSelectedItem().toString();
				data=Data.getUrlData(url,keyWord);
				
				if(Constant.SupportFuzzyUrl.indexOf(url)<Constant.division){
			
					ecDataModel = new DefaultTableModel(data, Constant.E_CommerceCcolumnNames){
						public void setValueAt(Object aValue, int row, int column){}
					};
					ecDataJT.setModel(ecDataModel);
					this.add(ecDataJSP);
				}else{
					page = 0;
					if(data.length>0){
						bnDataJTA.setText(data[0][0]);
					}
					bnDataJTA.setCaretPosition(0);
					this.add(upper);
					this.add(lower);
					this.add(bnDataJSP);
				}
				this.updateUI();
			}
		}
	}
	public void mouseClicked(MouseEvent e) {// 单击
		if ("dataDisplayRefresh".equals(e.getComponent().getName())) {
			selectUrl.removeAllItems();
			String[] urlSet=StringManipulation.oneDuplicateRemoval(StringManipulation.toOneDimensionalArrays(Data.getALLUrlSet()));
			for(String str:urlSet){//所有任务集
				selectUrl.addItem(str);
			}
			if(selectUrl.getItemCount()>0){
				selectKeyword.removeAllItems();
				for(String str:Data.getKeyWords(Data.getALLUrlSet(),selectUrl.getSelectedItem().toString())){
					selectKeyword.addItem(str);
				}
			}
			//数据清空
			ecDataModel = new DefaultTableModel(new String[0][], Constant.E_CommerceCcolumnNames){
				public void setValueAt(Object aValue, int row, int column){}
			};
			ecDataJT.setModel(ecDataModel);
			bnDataJTA.setText("");
			
		}else if ("upper".equals(e.getComponent().getName())) {
			if(data.length>0){
				page = (page+data.length-1)%data.length;
				bnDataJTA.setText(data[page][0]);
				bnDataJTA.setCaretPosition(0);
			}
		} else if ("lower".equals(e.getComponent().getName())) {
			if(data.length>0){
				page = (page+1)%data.length;
				bnDataJTA.setText(data[page][0]);
				bnDataJTA.setCaretPosition(0);
			}
		} 
	}

	public void mousePressed(MouseEvent e) {// 按下
	}

	public void mouseReleased(MouseEvent e) {// 释放
	}

	public void mouseEntered(MouseEvent e) {// 进入
		if ("dataDisplayRefresh".equals(e.getComponent().getName())) {
			dataDisplayRefresh.setBackground(Color.WHITE);
		}else if ("upper".equals(e.getComponent().getName())) {
			upper.setBackground(Color.WHITE);
		}else if ("lower".equals(e.getComponent().getName())) {
			lower.setBackground(Color.WHITE);
		}
	}

	public void mouseExited(MouseEvent e) {// 离开
		if ("dataDisplayRefresh".equals(e.getComponent().getName())) {
			dataDisplayRefresh.setBackground(Theme.ButtonColor);
		}else if ("upper".equals(e.getComponent().getName())) {
			upper.setBackground(Theme.ButtonColor);
		}else if ("lower".equals(e.getComponent().getName())) {
			lower.setBackground(Theme.ButtonColor);
		}
	}


}
