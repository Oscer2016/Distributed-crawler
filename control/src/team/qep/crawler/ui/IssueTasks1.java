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
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.table.DefaultTableModel;

import team.qep.crawler.server.Data;
import team.qep.crawler.server.Task;
import team.qep.crawler.util.Constant;
import team.qep.crawler.util.MyDocument;
import team.qep.crawler.util.StringManipulation;

public class IssueTasks1 extends JPanel implements MouseListener {
	private JLabel support = new JLabel("支 持 列 表");

	private JTable supportUrlSet = new JTable(new DefaultTableModel(
			StringManipulation.toTwoDimensionalArrays(Constant.SupportFuzzyUrl), new String[] { "SupportURL" }) {
		public boolean isCellEditable(int row, int column) {
			return false;
		}
	});
	private JScrollPane supportedJSP = new JScrollPane(supportUrlSet); // 支持的url集合
	private JLabel fuzzy = new JLabel("模  糊  爬  取");

	private JTextArea fuzzyURLSet = new JTextArea();
	private JScrollPane fuzzyURLSetJSP = new JScrollPane(fuzzyURLSet); // 待发布的模糊url集合
	private JComboBox<String> fuzzyUrlPriority = new JComboBox<String>(); // 模糊任务优先度
	private JButton fuzzyUrlPublish = new JButton(); // 模糊任务发布

	private JLabel exact = new JLabel("精  确  爬  取");
	private JComboBox<String> exactURLSet = new JComboBox<String>(); // 待发布的精确url
	private JTextField keyWord = new JTextField(); // 关键字
	private JComboBox<String> exactUrlPriority = new JComboBox<String>(); // 精确任务优先度
	private JButton exactUrlPublish = new JButton(); // 精确任务发布

	public IssueTasks1() {
		this.Init();
		this.loadingData();
		this.setBounds();
		this.setColour();
		this.listener();

		this.add(support);
		this.add(fuzzy);
		this.add(supportedJSP);
		this.add(fuzzyURLSetJSP);
		this.add(fuzzyUrlPriority);
		this.add(fuzzyUrlPublish);
		this.add(fuzzyUrlPublish);
		this.add(exact);
		this.add(exactURLSet);
		this.add(keyWord);
		this.add(exactUrlPriority);
		this.add(exactUrlPublish);
	}

	private void loadingData() {// 装载数据
		for (int i = 1; i <= 3; i++) {
			fuzzyUrlPriority.addItem("      优先级      " + String.valueOf(i));
			exactUrlPriority.addItem("      优先级      " + String.valueOf(i));
		}
		for (String str : Constant.SupportExactUrl) {
			exactURLSet.addItem(str);
		}
	}

	private void Init() {
		Init.initJTable(supportUrlSet, "supportUrlSet");
		Init.initJScrollPane(supportedJSP, "supportedJSP");

		Init.initJLable(support, "support");
		Init.initJLable(fuzzy, "fuzzy");
		Init.initJTextArea(fuzzyURLSet, "fuzzyURLSet");
		Init.initJScrollPane(fuzzyURLSetJSP, "fuzzyURLSetJSP");
		Init.initJComboBox(fuzzyUrlPriority, "fuzzyUrlPriority");
		Init.initJButton(fuzzyUrlPublish, "fuzzyUrlPublish");

		Init.initJLable(exact, "exact");
		Init.initJComboBox(exactURLSet, "exactURLSet");
		Init.initJTextField(keyWord, "keyWord");
		keyWord.setDocument(new MyDocument(30));
		Init.initJComboBox(exactUrlPriority, "exactUrlPriority");
		Init.initJButton(exactUrlPublish, "exactUrlPublish");
	}

	private void setBounds() {
		support.setBounds(55, 10, 200, 32);
		supportedJSP.setBounds(50, 60, 210, 480);

		fuzzy.setBounds(360, 10, 200, 32);
		fuzzyURLSetJSP.setBounds(350, 60, 230, 330);
		fuzzyUrlPriority.setBounds(365, 430, 200, 32);
		fuzzyUrlPublish.setBounds(380, 500, 170, 40);

		exact.setBounds(700, 10, 200, 35);
		exactURLSet.setBounds(680, 120, 230, 35);
		keyWord.setBounds(680, 225, 230, 35);
		exactUrlPriority.setBounds(695, 345, 200, 32);
		exactUrlPublish.setBounds(710, 450, 170, 40);
	}

	private void setColour() {
		this.setBackground(Theme.Panel1);

		support.setFont(Theme.TitleFont);
		support.setForeground(Theme.TitleColor);
		fuzzy.setFont(Theme.TitleFont);
		fuzzy.setForeground(Theme.TitleColor);
		fuzzyUrlPublish.setBackground(Theme.ButtonColor);
		fuzzyUrlPublish.setIcon(Constant.getIcon(fuzzyUrlPublish,"fuzzyUrlPublish"));

		exact.setFont(Theme.TitleFont);
		exact.setForeground(Theme.TitleColor);
		exactUrlPublish.setBackground(Theme.ButtonColor);
		exactUrlPublish.setIcon(Constant.getIcon(exactUrlPublish,"exactUrlPublish"));
	}

	private void listener() {
		supportUrlSet.addMouseListener(this);
		fuzzyUrlPublish.addMouseListener(this);
		exactUrlPublish.addMouseListener(this);
	}

	public void mouseClicked(MouseEvent e) {// 单击
		if ("supportUrlSet".equals(e.getComponent().getName())) {
			int selectedRow = supportUrlSet.getSelectedRow();
			if (selectedRow != -1) {
				fuzzyURLSet.append(supportUrlSet.getValueAt(selectedRow, 0).toString() + "\n");
			}
		} else if ("fuzzyUrlPublish".equals(e.getComponent().getName())) {
			String fuzzyURL = fuzzyURLSet.getText();
			int priority = fuzzyUrlPriority.getSelectedIndex() + 1;
			if (!fuzzyURL.equals("")) {
				int num=Data.isFfectiveResource();
				if(num>0){
					priority=Math.min(num,priority);
					if (Task.fuzzyUrlPublish(fuzzyURL, priority)) {
						new Promptinformation(null,"      模糊任务发布成功,已自动修正链接与去重",Constant.KeyValue.get("Info"));
						fuzzyURLSet.setText("");
						fuzzyUrlPriority.setSelectedIndex(0);
					} else {
						new Promptinformation(null, "      任务发送失败,已存在该任务", Constant.KeyValue.get("Info"));
					}
				}else{
					new Promptinformation(null, "      任务发送失败,无正在工作的从机,请添加一台从机", Constant.KeyValue.get("Info"));
				}
				
			} else {
				new Promptinformation(null, "      请输入url(可混合输入)", Constant.KeyValue.get("Info"));
			}
		} else if ("exactUrlPublish".equals(e.getComponent().getName())) {
			String exactURL = exactURLSet.getSelectedItem().toString();
			String key = keyWord.getText();
			int priority = exactUrlPriority.getSelectedIndex() + 1;

			if (!key.equals("")) {
				int num=Data.isFfectiveResource();
				if(num>0){
					if (Task.exactUrlPublish(exactURL, key, priority)) {
						new Promptinformation(null,"      精确任务发布成功",Constant.KeyValue.get("Info"));
						exactURLSet.setSelectedIndex(0);
						keyWord.setText("");
						exactUrlPriority.setSelectedIndex(0);
					} else {
						new Promptinformation(null, "      任务发送失败,已存在该任务", Constant.KeyValue.get("Info"));
					}
				}else{
					new Promptinformation(null, "      任务发送失败,无正在工作的从机,请添加一台从机", Constant.KeyValue.get("Info"));
				}
			} else {
				new Promptinformation(null, "      请输入关键字", Constant.KeyValue.get("Info"));
			}
		}
	}

	public void mousePressed(MouseEvent e) {// 按下
	}

	public void mouseReleased(MouseEvent e) {// 释放

	}

	public void mouseEntered(MouseEvent e) {// 进入
		if ("fuzzyUrlPublish".equals(e.getComponent().getName())) {
			fuzzyUrlPublish.setBackground(Color.WHITE);
		} else if ("exactUrlPublish".equals(e.getComponent().getName())) {
			exactUrlPublish.setBackground(Color.WHITE);
		}
	}

	public void mouseExited(MouseEvent e) {// 离开
		if ("fuzzyUrlPublish".equals(e.getComponent().getName())) {
			fuzzyUrlPublish.setBackground(Theme.ButtonColor);
		} else if ("exactUrlPublish".equals(e.getComponent().getName())) {
			exactUrlPublish.setBackground(Theme.ButtonColor);
		}
	}
}
