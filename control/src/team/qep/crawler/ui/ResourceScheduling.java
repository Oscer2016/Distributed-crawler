package team.qep.crawler.ui;

import java.awt.Color;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.table.DefaultTableModel;

import team.qep.crawler.server.Data;
import team.qep.crawler.server.Task;
import team.qep.crawler.util.Constant;
import team.qep.crawler.util.MyDocument;
import team.qep.crawler.util.Regex;
import team.qep.crawler.util.StringManipulation;

public class ResourceScheduling extends JPanel implements MouseListener {

	private JLabel resourceScheduling = new JLabel("资   源   配   置");//资源调度

	private String[] columnNames = Constant.ResourceSchedulingCcolumnNames; // 表格列名
	private String[][] data; // 表格数据
	private DefaultTableModel taskDataSetModel;
	private JTable resourcesSet = new JTable();//从机资源集合
	private JScrollPane resourcesJSP = new JScrollPane(resourcesSet); // 未终止的任务数据集
	
	private JButton resourceSchedulingRefresh = new JButton();// 刷新
	private JComboBox<String> ip = new JComboBox<String>();// 添加从机的ip
	private JButton add = new JButton();// 添加从机
	private JButton delete = new JButton();// 删除从机(只能删除未工作中的的从机)
	private JButton start = new JButton();// 重启从机(只能启用未工作状态/终止状态的机子)
	private JButton stop = new JButton();// 终止从机(只能终止工作中的的从机)

	public ResourceScheduling() {
		this.Init();
		this.loadingData();
		this.setBounds();
		this.setColour();
		this.listener();

		this.add(resourceScheduling);
		this.add(resourcesJSP);

		this.add(resourceSchedulingRefresh);
		this.add(ip);
		this.add(add);
		this.add(delete);
		this.add(start);
		this.add(stop);
	}

	private void loadingData() {// 装载数据
		taskDataSetModel = new DefaultTableModel(new String[0][], columnNames) {
			public boolean isCellEditable(int row, int column) {
				return false;
			}
		};
		resourcesSet.setModel(taskDataSetModel);
		
		for(String str:Constant.Resource){
			ip.addItem(str);
			Task.addDeleteResource(1,str);
		}
	}

	private void Init() {
		Init.initJLable(resourceScheduling, "resourceScheduling");

		Init.initJTable(resourcesSet, "resourcesSet");
		Init.initJScrollPane(resourcesJSP, "resourcesJSP");

		Init.initJButton(resourceSchedulingRefresh, "resourceSchedulingRefresh");
		Init.initJComboBox(ip,"ip");

		Init.initJButton(add, "add");
		Init.initJButton(delete, "delete");
		Init.initJButton(start,"start");
		Init.initJButton(stop,"stop");
	}

	private void setBounds() {
		resourceScheduling.setBounds(320, 0, 300, 35);
		
		resourcesJSP.setBounds(50, 50, 670, 520);
		
		resourceSchedulingRefresh.setBounds(770, 100, 150, 40);
		start.setBounds(770, 170, 150, 40);
		stop.setBounds(770,240, 150, 40);
		
		ip.setBounds(765, 340, 160, 35);
		add.setBounds(770, 410, 150, 40);
		delete.setBounds(770, 480, 150, 40);
		
	}

	private void setColour() {
		this.setBackground(Theme.Panel3);
		resourceScheduling.setFont(Theme.TitleFont);
		resourceScheduling.setForeground(Theme.TitleColor);
		
		resourceSchedulingRefresh.setBackground(Theme.ButtonColor);
		resourceSchedulingRefresh.setIcon(Constant.getIcon(resourceSchedulingRefresh,"resourceSchedulingRefresh"));
		add.setBackground(Theme.ButtonColor);
		add.setIcon(Constant.getIcon(add,"add"));
		delete.setBackground(Theme.ButtonColor);
		delete.setIcon(Constant.getIcon(delete,"delete"));
		start.setBackground(Theme.ButtonColor);
		start.setIcon(Constant.getIcon(start,"start"));
		stop.setBackground(Theme.ButtonColor);
		stop.setIcon(Constant.getIcon(stop,"stop"));
	}

	private void listener() {
		resourceSchedulingRefresh.addMouseListener(this);
		add.addMouseListener(this);
		delete.addMouseListener(this);
		start.addMouseListener(this);
		stop.addMouseListener(this);
	}

	public void mouseClicked(MouseEvent e) {// 单击
		if ("resourceSchedulingRefresh".equals(e.getComponent().getName())) {
			data=Data.getResourceInformation();
			taskDataSetModel = new DefaultTableModel(data, columnNames) {
				public boolean isCellEditable(int row, int column) {
					return false;
				}
			};
			resourcesSet.setModel(taskDataSetModel);
			
			for(int i=0 ; i<resourcesSet.getRowCount() ; i++){
				if(resourcesSet.getValueAt(i, 2).toString().equals("终止")){
	 				new Promptinformation(null, "      存在终止丛机,清立即进行重启或删除", Constant.KeyValue.get("Info"));
	 				resourcesSet.setRowSelectionInterval(i,i);
	 				break;
				}
			}
		} else if ("add".equals(e.getComponent().getName())) {
			if(!StringManipulation.duplicateDetection(Data.getResourceInformation(),ip.getSelectedItem().toString())){
				if(Task.addDeleteResource(1,ip.getSelectedItem().toString())){
					new Promptinformation(null, "      添加成功,请重启从机使之正常工作", Constant.KeyValue.get("Info"));
				
					data=Data.getResourceInformation();
					taskDataSetModel = new DefaultTableModel(data, columnNames){
						public boolean isCellEditable(int row, int column) {
							return false;
						}
					};
					resourcesSet.setModel(taskDataSetModel);
				}
			}else{
 				new Promptinformation(null, "      添加失败,该从机已添加过", Constant.KeyValue.get("Info"));
			}
		} else if ("delete".equals(e.getComponent().getName())) {
			int selectedRow = resourcesSet.getSelectedRow();
			if (selectedRow != -1) {
				String status=resourcesSet.getValueAt(selectedRow, 2).toString();
				if(status.equals("未工作") || status.equals("终止")){
					new Promptinformation(null, "      是否删除此台从机?", Constant.KeyValue.get("Confirm"));
					if(Promptinformation.flag){
						if(Task.addDeleteResource(0,resourcesSet.getValueAt(selectedRow, 0).toString())){
							new Promptinformation(null, "      删除成功", Constant.KeyValue.get("Info"));
						
							data=Data.getResourceInformation();
							taskDataSetModel = new DefaultTableModel(data, columnNames) {
								public boolean isCellEditable(int row, int column) {
									return false;
								}
							};
							resourcesSet.setModel(taskDataSetModel);
						}
					}
				}else{
					new Promptinformation(null, "      无法删除正在工作的从机", Constant.KeyValue.get("Info"));
				}
			}
		} else if ("start".equals(e.getComponent().getName())) {
			//只能启用状态为未工作的  
			int selectedRow = resourcesSet.getSelectedRow();
			if (selectedRow != -1) {
				if(resourcesSet.getValueAt(selectedRow, 2).toString().equals("未工作") || resourcesSet.getValueAt(selectedRow, 2).toString().equals("终止")){
					if(Task.modifyResourceStatus(resourcesSet.getValueAt(selectedRow, 0).toString(),Constant.KeyValue.get("Start"))){
						
						try {
							Thread.sleep(1500);
						} catch (InterruptedException e1) {
							e1.printStackTrace();
						}
						
						data=Data.getResourceInformation();
						taskDataSetModel = new DefaultTableModel(data, columnNames) {
							public boolean isCellEditable(int row, int column) {
								return false;
							}
						};
						resourcesSet.setModel(taskDataSetModel);
						
						new Promptinformation(null, "      重启成功", Constant.KeyValue.get("Info"));
					}
				}else{
					new Promptinformation(null, "      无法重启,请重新选择", Constant.KeyValue.get("Info"));
				}
			}
		}else if ("stop".equals(e.getComponent().getName())) {
			//只能终止状态为工作中的  
			int selectedRow = resourcesSet.getSelectedRow();
			if (selectedRow != -1) {
				if(resourcesSet.getValueAt(selectedRow, 2).toString().equals("工作中")){
					if(Task.modifyResourceStatus(resourcesSet.getValueAt(selectedRow, 0).toString(),Constant.KeyValue.get("Stop"))){
						
						try {
							Thread.sleep(1000);
						} catch (InterruptedException e1) {
							e1.printStackTrace();
						}
						
						data=Data.getResourceInformation();
						taskDataSetModel = new DefaultTableModel(data, columnNames) {
							public boolean isCellEditable(int row, int column) {
								return false;
							}
						};
						resourcesSet.setModel(taskDataSetModel);
						
						new Promptinformation(null, "      终止成功", Constant.KeyValue.get("Info"));
					}
				}else{
					new Promptinformation(null, "      无法终止,请重新选择", Constant.KeyValue.get("Info"));
				}
			}
		}
	}
	public void mousePressed(MouseEvent e) {// 按下
	}

	public void mouseReleased(MouseEvent e) {// 释放
	}

	public void mouseEntered(MouseEvent e) {// 进入
		if ("resourceSchedulingRefresh".equals(e.getComponent().getName())) {
			resourceSchedulingRefresh.setBackground(Color.WHITE);
		} else if ("add".equals(e.getComponent().getName())) {
			add.setBackground(Color.WHITE);
		} else if ("delete".equals(e.getComponent().getName())) {
			delete.setBackground(Color.WHITE);
		} else if ("start".equals(e.getComponent().getName())) {
			start.setBackground(Color.WHITE);
		} else if ("stop".equals(e.getComponent().getName())) {
			stop.setBackground(Color.WHITE);
		}
	}

	public void mouseExited(MouseEvent e) {// 离开
		if ("resourceSchedulingRefresh".equals(e.getComponent().getName())) {
			resourceSchedulingRefresh.setBackground(Theme.ButtonColor);
		}else if ("add".equals(e.getComponent().getName())) {
			add.setBackground(Theme.ButtonColor);
		} else if ("delete".equals(e.getComponent().getName())) {
			delete.setBackground(Theme.ButtonColor);
		} else if ("start".equals(e.getComponent().getName())) {
			start.setBackground(Theme.ButtonColor);
		}else if ("stop".equals(e.getComponent().getName())) {
			stop.setBackground(Theme.ButtonColor);
		}
	}
}
