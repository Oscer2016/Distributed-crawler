package team.qep.crawler.ui;

import java.awt.Color;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.table.DefaultTableModel;
import team.qep.crawler.server.Data;
import team.qep.crawler.server.Task;
import team.qep.crawler.util.Constant;

public class TaskControl extends JPanel implements MouseListener {

	private JLabel task = new JLabel("任   务   中  心");

	private String[][] data; // 表格数据
	private DefaultTableModel taskDataSetModel;
	private JTable taskDataSet = new JTable();
	private JScrollPane taskDataJSP = new JScrollPane(taskDataSet); // 未终止的任务数据集
	
	private JButton TaskControlRefresh = new JButton();// 刷新
	private JButton startTask = new JButton();// 开始任务
	private JButton suspendTask = new JButton();// 暂停任务
	private JButton endTask = new JButton();// 结束任务

	public TaskControl() {
		this.Init();
		this.loadingData();
		this.setBounds();
		this.setColour();
		this.listener();

		this.add(task);
		this.add(taskDataJSP);

		this.add(TaskControlRefresh);
		this.add(startTask);
		this.add(suspendTask);
		this.add(endTask);
	}

	private void loadingData() {// 装载数据
		taskDataSetModel = new DefaultTableModel(new String[0][], Constant.TaskCcolumnNames) {
			public boolean isCellEditable(int row, int column) {
				return false;
			}
		};
		taskDataSet.setModel(taskDataSetModel);
	}

	private void Init() {
		Init.initJLable(task, "task");

		Init.initJTable(taskDataSet, "taskDataSet");
		Init.initJScrollPane(taskDataJSP, "taskDataJSP");
		Init.initJButton(TaskControlRefresh, "TaskControlRefresh");
		Init.initJButton(startTask, "startTask");
		Init.initJButton(suspendTask, "suspendTask");
		Init.initJButton(endTask, "endTask");
	}

	private void setBounds() {
		task.setBounds(320, 0, 300, 35);
		taskDataJSP.setBounds(20, 50, 934, 420);

		TaskControlRefresh.setBounds(40, 515, 150, 40);
		startTask.setBounds(290, 515, 150, 40);
		suspendTask.setBounds(535, 515, 150, 40);
		endTask.setBounds(780, 515, 150, 40);
	}

	private void setColour() {
		this.setBackground(Theme.Panel4);

		task.setFont(Theme.TitleFont);
		task.setForeground(Theme.TitleColor);
		TaskControlRefresh.setBackground(Theme.ButtonColor);
		TaskControlRefresh.setIcon(Constant.getIcon(TaskControlRefresh,"TaskControlRefresh"));
		startTask.setBackground(Theme.ButtonColor);
		startTask.setIcon(Constant.getIcon(startTask,"startTask"));
		suspendTask.setBackground(Theme.ButtonColor);
		suspendTask.setIcon(Constant.getIcon(suspendTask,"suspendTask"));
		endTask.setBackground(Theme.ButtonColor);
		endTask.setIcon(Constant.getIcon(endTask,"endTask"));
		taskDataSet.setFont(Theme.Tablefont);// 设置字体格式
	}

	private void listener() {
		TaskControlRefresh.addMouseListener(this);
		startTask.addMouseListener(this);
		suspendTask.addMouseListener(this);
		endTask.addMouseListener(this);
	}

	public void mouseClicked(MouseEvent e) {// 单击
		if ("TaskControlRefresh".equals(e.getComponent().getName())) {
			data=Data.getRunUrlSet();
			taskDataSetModel = new DefaultTableModel(data,  Constant.TaskCcolumnNames) {
				public boolean isCellEditable(int row, int column) {
					return false;
				}
			};
			taskDataSet.setModel(taskDataSetModel);
		} else if ("startTask".equals(e.getComponent().getName())) {
			//只能开始任务状态为暂停的  
			int selectedRow = taskDataSet.getSelectedRow();
			if (selectedRow != -1) {
				if(taskDataSet.getValueAt(selectedRow, 5).toString().equals("暂停中")){
					if(Task.modifyTaskStatus(taskDataSet.getValueAt(selectedRow, 0).toString(),taskDataSet.getValueAt(selectedRow, 1).toString(),Constant.KeyValue.get("Run"))){

						data=Data.getRunUrlSet();
						taskDataSetModel = new DefaultTableModel(data,  Constant.TaskCcolumnNames) {
							public boolean isCellEditable(int row, int column) {
								return false;
							}
						};
						taskDataSet.setModel(taskDataSetModel);
						
						new Promptinformation(null, "      任务运行成功", Constant.KeyValue.get("Info"));
					}
				}else{
					new Promptinformation(null, "      无法运行,请重新选择", Constant.KeyValue.get("Info"));
				}
			}
		} else if ("suspendTask".equals(e.getComponent().getName())) {
			//只能暂停任务状态为运行中  
			int selectedRow = taskDataSet.getSelectedRow();
			if (selectedRow != -1) {
				if(taskDataSet.getValueAt(selectedRow, 5).toString().equals("运行中")){
					if(Task.modifyTaskStatus(taskDataSet.getValueAt(selectedRow, 0).toString(),taskDataSet.getValueAt(selectedRow, 1).toString(),Constant.KeyValue.get("Wait"))){

						data=Data.getRunUrlSet();
						taskDataSetModel = new DefaultTableModel(data,  Constant.TaskCcolumnNames) {
							public boolean isCellEditable(int row, int column) {
								return false;
							}
						};
						taskDataSet.setModel(taskDataSetModel);
						
						new Promptinformation(null, "      任务暂停成功", Constant.KeyValue.get("Info"));
					}
				}else{
					new Promptinformation(null, "      无法暂停,请重新选择", Constant.KeyValue.get("Info"));
				}
			}
		} else if ("endTask".equals(e.getComponent().getName())) {
			int selectedRow = taskDataSet.getSelectedRow();
			if (selectedRow != -1) {
				new Promptinformation(null, "确定要终止此任务?", Constant.KeyValue.get("Confirm"));
				if(Promptinformation.flag){
					if(Task.modifyTaskStatus(taskDataSet.getValueAt(selectedRow, 0).toString(),taskDataSet.getValueAt(selectedRow, 1).toString(),Constant.KeyValue.get("Complete"))){
						data=Data.getRunUrlSet();
						taskDataSetModel = new DefaultTableModel(data,  Constant.TaskCcolumnNames) {
							public boolean isCellEditable(int row, int column) {
								return false;
							}
						};
						taskDataSet.setModel(taskDataSetModel);
						new Promptinformation(null, "      任务终止成功", Constant.KeyValue.get("Info"));
					}
				}
			}
		}
	}

	public void mousePressed(MouseEvent e) {// 按下
	}

	public void mouseReleased(MouseEvent e) {// 释放
	}

	public void mouseEntered(MouseEvent e) {// 进入
		if ("TaskControlRefresh".equals(e.getComponent().getName())) {
			TaskControlRefresh.setBackground(Color.WHITE);
		} else if ("startTask".equals(e.getComponent().getName())) {
			startTask.setBackground(Color.WHITE);
		} else if ("suspendTask".equals(e.getComponent().getName())) {
			suspendTask.setBackground(Color.WHITE);
		} else if ("endTask".equals(e.getComponent().getName())) {
			endTask.setBackground(Color.WHITE);
		}
	}

	public void mouseExited(MouseEvent e) {// 离开
		if ("TaskControlRefresh".equals(e.getComponent().getName())) {
			TaskControlRefresh.setBackground(Theme.ButtonColor);
		}else if ("startTask".equals(e.getComponent().getName())) {
			startTask.setBackground(Theme.ButtonColor);
		} else if ("suspendTask".equals(e.getComponent().getName())) {
			suspendTask.setBackground(Theme.ButtonColor);
		} else if ("endTask".equals(e.getComponent().getName())) {
			endTask.setBackground(Theme.ButtonColor);
		}
	}
}
